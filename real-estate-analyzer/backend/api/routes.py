import re
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from api.auth_routes import get_current_user
from api.schemas import AnalyzeRequest, AnalyzeResponse
from db.database import get_db
from db.models import AgentLog, Analysis, Results, SavedReport, User
from tasks import AGENT_STEPS, execute_pipeline, run_analysis, seed_agent_logs

router = APIRouter(tags=["analysis"])


def zip_from_address(address: str) -> str:
    match = re.search(r"\b\d{5}\b", address)
    return match.group(0) if match else "78702"


def require_owned_analysis(db: Session, user: User, analysis_id: int) -> Analysis:
    analysis = db.get(Analysis, analysis_id)
    if analysis is None or analysis.user_id != user.id:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


@router.post("/analyze", response_model=AnalyzeResponse)
def create_analysis(
    payload: AnalyzeRequest,
    background_tasks: BackgroundTasks,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> AnalyzeResponse:
    address = payload.address.strip()
    if not address:
        raise HTTPException(status_code=422, detail="Address is required")
    analysis = Analysis(user_id=user.id, address=address, zip_code=zip_from_address(address), status="pending")
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    seed_agent_logs(db, analysis.id)
    try:
        run_analysis.delay(analysis.id, address)
    except Exception:
        background_tasks.add_task(execute_pipeline, analysis.id, address)
    return AnalyzeResponse(analysis_id=analysis.id)


@router.get("/analyze/{analysis_id}/status")
def analysis_status(
    analysis_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> dict:
    analysis = require_owned_analysis(db, user, analysis_id)
    logs = db.query(AgentLog).filter_by(analysis_id=analysis_id).all()
    by_name = {log.agent_name: log for log in logs}
    agents = []
    for name, default_log in AGENT_STEPS:
        log = by_name.get(name)
        agents.append(
            {
                "name": name,
                "status": log.status if log else "waiting",
                "log": log.log_message if log else default_log,
                "duration": log.duration if log else 0,
            }
        )
    return {"agents": agents, "complete": analysis.status == "complete", "address": analysis.address, "status": analysis.status}


@router.get("/analyze/{analysis_id}/results")
def analysis_results(
    analysis_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> dict:
    analysis = require_owned_analysis(db, user, analysis_id)
    results = db.query(Results).filter_by(analysis_id=analysis_id).first()
    if results is None:
        raise HTTPException(status_code=404, detail="Results are not ready yet")
    return {
        "id": analysis.id,
        "address": analysis.address,
        "market_data": results.market_data,
        "financial_data": results.financial_data,
        "zoning_data": results.zoning_data,
        "risk_data": results.risk_data,
        "report_data": results.report_data,
    }


@router.get("/analyze/{analysis_id}/report")
def analysis_report(
    analysis_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> dict:
    require_owned_analysis(db, user, analysis_id)
    results = db.query(Results).filter_by(analysis_id=analysis_id).first()
    if results is None:
        raise HTTPException(status_code=404, detail="Report is not ready yet")
    return {
        "memo_markdown": results.report_data.get("memo_markdown", ""),
        "verdict": results.report_data.get("verdict", "Proceed with Caution"),
        "recommendation": results.report_data.get("recommendation", ""),
    }


@router.patch("/analyze/{analysis_id}/save")
def save_report(
    analysis_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> dict[str, bool]:
    require_owned_analysis(db, user, analysis_id)
    existing = db.query(SavedReport).filter_by(analysis_id=analysis_id, user_id=user.id).first()
    if existing is None:
        db.add(SavedReport(analysis_id=analysis_id, user_id=user.id))
        db.commit()
    return {"saved": True}


@router.get("/history")
def history(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> list[dict[str, str | int]]:
    analyses = db.query(Analysis).filter_by(user_id=user.id).order_by(Analysis.created_at.desc()).all()
    return [
        {
            "id": analysis.id,
            "address": analysis.address,
            "status": analysis.status,
            "created_at": analysis.created_at.isoformat(),
        }
        for analysis in analyses
    ]

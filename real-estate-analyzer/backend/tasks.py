import asyncio
import os
import time
from datetime import datetime

from celery import Celery
from sqlalchemy.orm import Session

from agents.financial_agent import run_financial_agent
from agents.market_agent import run_market_agent
from agents.report_agent import run_report_agent
from agents.risk_agent import run_risk_agent
from agents.zoning_agent import run_zoning_agent
from db.database import SessionLocal
from db.models import AgentLog, Analysis, Results

celery = Celery("real_estate_analyzer", broker=os.getenv("REDIS_URL", "redis://redis:6379/0"))

AGENT_STEPS = [
    ("Market Agent", "Fetching property comps & neighborhood data"),
    ("Financial Agent", "Computing ROI, Cap Rate, Cash-on-Cash"),
    ("Zoning Agent", "Checking zoning codes & permit history"),
    ("Risk Agent", "Evaluating vacancy, flood zone, walk score"),
    ("Report Agent", "Generating investment memo with GPT-4o"),
]


def seed_agent_logs(db: Session, analysis_id: int) -> None:
    for name, message in AGENT_STEPS:
        existing = db.query(AgentLog).filter_by(analysis_id=analysis_id, agent_name=name).first()
        if existing is None:
            db.add(AgentLog(analysis_id=analysis_id, agent_name=name, status="waiting", log_message=message))
    db.commit()


def update_log(db: Session, analysis_id: int, agent_name: str, status: str, message: str, started: float | None = None) -> None:
    log = db.query(AgentLog).filter_by(analysis_id=analysis_id, agent_name=agent_name).first()
    if log is None:
        log = AgentLog(analysis_id=analysis_id, agent_name=agent_name)
        db.add(log)
    log.status = status
    log.log_message = message
    if status == "running":
        log.started_at = datetime.utcnow()
    if status in {"done", "failed"}:
        log.completed_at = datetime.utcnow()
        if started is not None:
            log.duration = max(1, round(time.perf_counter() - started))
    db.commit()


async def execute_pipeline(analysis_id: int, address: str) -> None:
    db = SessionLocal()
    try:
        analysis = db.get(Analysis, analysis_id)
        if analysis is None:
            return
        analysis.status = "running"
        seed_agent_logs(db, analysis_id)
        db.commit()

        start = time.perf_counter()
        update_log(db, analysis_id, "Market Agent", "running", "Fetching ATTOM comps and Census neighborhood signals")
        market = await run_market_agent(address)
        update_log(db, analysis_id, "Market Agent", "done", "Market data complete", start)

        start = time.perf_counter()
        update_log(db, analysis_id, "Financial Agent", "running", "Calculating NOI, cap rate, cash-on-cash, and GRM")
        financial = await run_financial_agent(address)
        update_log(db, analysis_id, "Financial Agent", "done", "Financial model complete", start)

        start = time.perf_counter()
        update_log(db, analysis_id, "Zoning Agent", "running", "Reviewing zone code, permitted uses, and permit activity")
        zoning = await run_zoning_agent(address)
        update_log(db, analysis_id, "Zoning Agent", "done", "Zoning review complete", start)

        start = time.perf_counter()
        update_log(db, analysis_id, "Risk Agent", "running", "Scoring vacancy, flood, crime, mobility, and macro risks")
        risk = await run_risk_agent(address)
        update_log(db, analysis_id, "Risk Agent", "done", "Risk assessment complete", start)

        start = time.perf_counter()
        update_log(db, analysis_id, "Report Agent", "running", "Synthesizing final investment memo")
        report = await run_report_agent(market, financial, zoning, risk)
        update_log(db, analysis_id, "Report Agent", "done", "Investment memo complete", start)

        existing = db.query(Results).filter_by(analysis_id=analysis_id).first()
        if existing is None:
            existing = Results(analysis_id=analysis_id)
            db.add(existing)
        existing.market_data = market
        existing.financial_data = financial
        existing.zoning_data = zoning
        existing.risk_data = risk
        existing.report_data = report
        analysis.status = "complete"
        analysis.completed_at = datetime.utcnow()
        db.commit()
    except Exception as exc:
        analysis = db.get(Analysis, analysis_id)
        if analysis is not None:
            analysis.status = "failed"
            db.commit()
        raise exc
    finally:
        db.close()


@celery.task(name="tasks.run_analysis")
def run_analysis(analysis_id: int, address: str) -> None:
    asyncio.run(execute_pipeline(analysis_id, address))


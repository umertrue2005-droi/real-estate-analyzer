from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from db.database import Base, engine

JsonType = JSONB if engine.dialect.name == "postgresql" else JSON


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    analyses: Mapped[list["Analysis"]] = relationship(back_populates="user")


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(12), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    user: Mapped[User] = relationship(back_populates="analyses")
    logs: Mapped[list["AgentLog"]] = relationship(back_populates="analysis", cascade="all, delete-orphan")
    results: Mapped["Results | None"] = relationship(back_populates="analysis", cascade="all, delete-orphan")


class AgentLog(Base):
    __tablename__ = "agent_logs"
    __table_args__ = (UniqueConstraint("analysis_id", "agent_name", name="uq_analysis_agent"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey("analyses.id"), nullable=False)
    agent_name: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="waiting", nullable=False)
    log_message: Mapped[str] = mapped_column(Text, default="", nullable=False)
    duration: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    analysis: Mapped[Analysis] = relationship(back_populates="logs")


class Results(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey("analyses.id"), unique=True, nullable=False)
    market_data: Mapped[dict] = mapped_column(MutableDict.as_mutable(JsonType), default=dict, nullable=False)
    financial_data: Mapped[dict] = mapped_column(MutableDict.as_mutable(JsonType), default=dict, nullable=False)
    zoning_data: Mapped[dict] = mapped_column(MutableDict.as_mutable(JsonType), default=dict, nullable=False)
    risk_data: Mapped[dict] = mapped_column(MutableDict.as_mutable(JsonType), default=dict, nullable=False)
    report_data: Mapped[dict] = mapped_column(MutableDict.as_mutable(JsonType), default=dict, nullable=False)

    analysis: Mapped[Analysis] = relationship(back_populates="results")


class SavedReport(Base):
    __tablename__ = "saved_reports"
    __table_args__ = (UniqueConstraint("analysis_id", "user_id", name="uq_saved_report"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey("analyses.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    saved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


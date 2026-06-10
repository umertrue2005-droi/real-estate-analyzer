"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-06-08
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def json_type():
    return postgresql.JSONB(astext_type=sa.Text())


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_table(
        "analyses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("zip_code", sa.String(length=12), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_analyses_id"), "analyses", ["id"], unique=False)
    op.create_table(
        "agent_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("analysis_id", sa.Integer(), nullable=False),
        sa.Column("agent_name", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("log_message", sa.Text(), nullable=False),
        sa.Column("duration", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["analysis_id"], ["analyses.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_id", "agent_name", name="uq_analysis_agent"),
    )
    op.create_index(op.f("ix_agent_logs_id"), "agent_logs", ["id"], unique=False)
    op.create_table(
        "results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("analysis_id", sa.Integer(), nullable=False),
        sa.Column("market_data", json_type(), nullable=False),
        sa.Column("financial_data", json_type(), nullable=False),
        sa.Column("zoning_data", json_type(), nullable=False),
        sa.Column("risk_data", json_type(), nullable=False),
        sa.Column("report_data", json_type(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_id"], ["analyses.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_id"),
    )
    op.create_index(op.f("ix_results_id"), "results", ["id"], unique=False)
    op.create_table(
        "saved_reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("analysis_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("saved_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_id"], ["analyses.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("analysis_id", "user_id", name="uq_saved_report"),
    )
    op.create_index(op.f("ix_saved_reports_id"), "saved_reports", ["id"], unique=False)


def downgrade() -> None:
    op.drop_table("saved_reports")
    op.drop_table("results")
    op.drop_table("agent_logs")
    op.drop_table("analyses")
    op.drop_table("users")


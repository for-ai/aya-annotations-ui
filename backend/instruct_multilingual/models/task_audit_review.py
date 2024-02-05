from datetime import datetime
from typing import Optional
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_psql

from sqlmodel import Field, SQLModel


class TaskAuditReview(SQLModel, table=True):
    __tablename__ = "task_audit_review"

    id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            primary_key=True,
            server_default=(sa.text("uuid_generate_v4()")),
        ),
    )
    task_audit_id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            sa.ForeignKey("task_audit.id"),
            nullable=False,
        ),
    )
    edited_prompt_rating: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )
    edited_completion_rating: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )
    improved_prompt: Optional[str] = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=True,
        ),
    )
    improved_completion: Optional[str] = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=True,
        ),
    )
    improvement_feedback: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        ),
    )
    submitted_by: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            nullable=False,
        ),
    )
    created_at: datetime = Field(
        sa_column=sa.Column(
            sa.DateTime,
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

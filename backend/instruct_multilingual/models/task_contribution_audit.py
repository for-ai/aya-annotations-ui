from datetime import datetime
from typing import Optional
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_psql

from sqlmodel import Field, SQLModel


class TaskContributionAudit(SQLModel, table=True):
    __tablename__ = "task_contribution_audit"

    id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            primary_key=True,
            server_default=(sa.text("uuid_generate_v4()")),
        ),
    )
    task_contribution_id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            sa.ForeignKey("task_contribution.id"),
            nullable=False,
        ),
    )
    submitted_by: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            sa.ForeignKey("user.id"),
            nullable=False,
        ),
    )
    submitted_prompt: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        ),
    )
    submitted_completion: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        ),
    )
    prompt_edited: bool = Field(
        sa_column=sa.Column(
            sa.Boolean,
            nullable=False,
        ),
    )
    completion_edited: bool = Field(
        sa_column=sa.Column(
            sa.Boolean,
            nullable=False,
        ),
    )
    prompt_rating: Optional[int] = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )
    completion_rating: Optional[int] = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )
    edit_distance: Optional[float] = Field(
        sa_column=sa.Column(
            sa.DECIMAL,
            nullable=True,
        ),
    )
    created_at: Optional[datetime] = Field(
        sa_column=sa.Column(
            sa.DateTime,
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

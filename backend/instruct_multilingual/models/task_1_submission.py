from datetime import datetime
from typing import Optional
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_psql

from sqlmodel import Field, SQLModel


class Task1Submission(SQLModel, table=True):
    __tablename__ = "task_1_submission"

    id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            primary_key=True,
        ),
    )
    submitted_by: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            nullable=False,
        ),
    )
    submitted_prompt: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        )
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
        )
    )
    completion_edited: bool = Field(
        sa_column=sa.Column(
            sa.Boolean,
            nullable=False,
        )
    )
    prompt_rating: Optional[int] = Field(
        sa_column=sa.Column(
            sa.Integer,
        ),
    )
    completion_rating: Optional[int] = Field(
        sa_column=sa.Column(
            sa.Integer,
        ),
    )
    created_at: datetime = Field(
        sa_column=sa.Column(
            sa.DateTime,
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    edit_distance: Optional[float] = Field(
        sa_column=sa.Column(
            sa.Float,
        ),
    )

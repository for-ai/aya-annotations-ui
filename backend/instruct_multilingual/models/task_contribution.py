from datetime import datetime
from typing import Optional
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_psql

from sqlmodel import Field, SQLModel


class TaskContribution(SQLModel, table=True):
    __tablename__ = "task_contribution"

    id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            primary_key=True,
            server_default=(sa.text("uuid_generate_v4()")),
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
    language_id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            sa.ForeignKey("language_code.id"),
            nullable=False,
        ),
    )
    created_at: Optional[datetime] = Field(
        sa_column=sa.Column(
            sa.DateTime,
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

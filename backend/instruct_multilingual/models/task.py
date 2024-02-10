from datetime import datetime
from typing import Optional
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_psql

from sqlmodel import Field, Relationship, SQLModel


class Task(SQLModel, table=True):
    __tablename__ = "task"

    id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            primary_key=True,
            server_default=(sa.text("uuid_generate_v4()")),
        ),
    )
    prompt: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        )
    )
    completion: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        ),
    )
    task_type: Optional[str] = Field(
        sa_column=sa.Column(
            sa.Enum("audit_translation", "audit_xp3", name="task_type"),
            nullable=False,
        ),
    )
    dataset_id: Optional[UUID] = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            sa.ForeignKey("dataset.id"),
            nullable=False,
        ),
    )
    language_id: Optional[UUID] = Field(
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

    key_hash: Optional[str] = Field(
        sa_column=sa.Column(
            sa.String(length=64),
            nullable=False,
        ),
    )

    __table_args__ = (
        sa.UniqueConstraint('prompt', 'completion'),
    )

    dataset: Optional["Dataset"] = Relationship(back_populates="tasks")

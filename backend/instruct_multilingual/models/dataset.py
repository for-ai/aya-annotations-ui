from datetime import datetime
from typing import List, Optional
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_psql

from sqlmodel import Field, Relationship, SQLModel


class Dataset(SQLModel, table=True):
    __tablename__ = "dataset"

    id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            primary_key=True,
            server_default=(sa.text("uuid_generate_v4()")),
        ),
    )
    name: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        )
    )
    language_id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            sa.ForeignKey("language_code.id"),
            nullable=False,
        ),
    )
    translated: bool = Field(
        sa_column=sa.Column(
            sa.Boolean,
            nullable=False,
        ),
    )
    templated: bool = Field(
        sa_column=sa.Column(
            sa.Boolean,
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
    tasks: List["Task"] = Relationship(back_populates="dataset")

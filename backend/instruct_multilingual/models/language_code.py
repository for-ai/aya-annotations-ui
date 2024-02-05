from datetime import datetime
from typing import List, Optional
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_psql

from sqlmodel import Field, SQLModel


class LanguageCode(SQLModel, table=True):
    __tablename__ = "language_code"

    id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            primary_key=True,
            server_default=(sa.text("uuid_generate_v4()")),
        ),
    )
    code: str = Field(
        sa_column=sa.Column(
            sa_psql.VARCHAR(2),
            nullable=False,
        )
    )
    name: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        )
    )
    character_code: str = Field(
        sa_column=sa.Column(
            sa_psql.VARCHAR(5),
            nullable=False,
        )
    )
    direction: Optional[str] = Field(
        sa_column=sa.Column(
            sa.Enum("ltr", "rtl", name="direction"),
            nullable=True,
        )
    )
    created_at: Optional[datetime] = Field(
        sa_column=sa.Column(
            sa.DateTime,
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

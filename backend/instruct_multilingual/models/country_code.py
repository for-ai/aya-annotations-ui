from datetime import datetime
from typing import List, Optional
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_psql

from sqlmodel import Field, SQLModel


class CountryCode(SQLModel, table=True):
    __tablename__ = "country_code"

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
    created_at: Optional[datetime] = Field(
        sa_column=sa.Column(
            sa.DateTime,
            nullable=False,
            server_default=sa.func.now(),
        ),  
    )

    __table_args__ = (
        sa.UniqueConstraint("code", name="country_code_code_key"),
        sa.UniqueConstraint("name", name="country_code_name_key"),
    )

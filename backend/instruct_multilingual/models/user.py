from datetime import datetime
from typing import List, Optional
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_psql

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            primary_key=True,
            server_default=(sa.text("uuid_generate_v4()")),
        ),
    )
    # discord ids are "snowflake" ids
    # https://discord.com/developers/docs/reference?ref=blog.netcord.in#snowflakes
    # we'll store them as strings to avoid having to create custom types
    discord_id: str = Field(
        sa_column=sa.Column(
            sa.String(),
            nullable=True,
        )
    )
    google_id: str = Field(
        sa_column=sa.Column(
            sa.String(),
            nullable=True,
        )
    )
    username: str = Field(
        sa_column=sa.Column(
            sa_psql.VARCHAR(64),
            nullable=False,
        )
    )
    email: Optional[str] = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=True,
        )
    )
    image_url: str = Field(
        sa_column=sa.Column(
            sa_psql.VARCHAR(256),
            nullable=False,
        )
    )
    country_code: Optional[UUID] = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            sa.ForeignKey("country_code.id"),
            nullable=True,
        ),
    )
    language_codes: Optional[List[UUID]] = Field(
        sa_column=sa.Column(
            sa.ARRAY(sa_psql.UUID(as_uuid=True)),
            nullable=True,
        ),
    )
    # 0 to infinity (no upper bound)
    # https://docs.sqlalchemy.org/en/14/core/custom_types.html#sqlalchemy.types.RangeType
    # inclusive lower bound, inclusive upper bound
    age_range: Optional[int] = Field(
        sa_column=sa.Column(
            sa_psql.INT4RANGE,
            nullable=True,
        ),
    )
    gender: Optional[str] = Field(
        sa_column=sa.Column(
            sa_psql.VARCHAR(64),
            nullable=True,
        ),
    )
    dialects: Optional[List[str]] = Field(
        sa_column=sa.Column(
            sa.ARRAY(sa.String(50)),
            nullable=True
        )
    )
    created_at: Optional[datetime] = Field(
        sa_column=sa.Column(
            sa.DateTime,
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

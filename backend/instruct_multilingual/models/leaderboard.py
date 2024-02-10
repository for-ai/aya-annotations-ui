from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_psql

from sqlmodel import Field, SQLModel


class LeaderboardDaily(SQLModel, table=True):
    __tablename__ = "leaderboard_daily"

    id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            primary_key=True,
            server_default=(sa.text("uuid_generate_v4()")),
        ),
    )
    user_id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            nullable=False,
        ),
    )
    username: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        ),
    )
    languages: List[str] = Field(
        sa_column=sa.Column(
            sa.ARRAY(sa.Text),
        ),
        # NOTE: this is nullable temporarily while
        # we don't have to backfill leaderboard data yet
        nullable=True,
    )
    image_url: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        ),
    )
    day: date = Field(
        sa_column=sa.Column(
            sa.Date,
            nullable=False,
        ),
    )
    rank: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )
    points: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )


class LeaderboardWeekly(SQLModel, table=True):
    __tablename__ = "leaderboard_weekly"

    id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            primary_key=True,
            server_default=(sa.text("uuid_generate_v4()")),
        ),
    )
    user_id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            nullable=False,
        ),
    )
    username: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        ),
    )
    languages: List[str] = Field(
        sa_column=sa.Column(
            sa.ARRAY(sa.Text),
        ),
        # NOTE: this is nullable temporarily while
        # we don't have to backfill leaderboard data yet
        nullable=True,
    )
    image_url: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        ),
    )
    week_of: date = Field(
        sa_column=sa.Column(
            sa.Date,
            nullable=False,
        ),
    )
    rank: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )
    points: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )


class LeaderboardByLanguage(SQLModel, table=True):
    __tablename__ = "leaderboard_by_language"

    id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            primary_key=True,
            server_default=(sa.text("uuid_generate_v4()")),
        ),
    )
    user_id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            nullable=False,
        ),
    )
    username: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        ),
    )
    image_url: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        ),
    )
    language: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        ),
    )
    language_code: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        ),
    )
    rank: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )
    points: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )
    blended_rank: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )
    blended_points: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )
    quality_score: Optional[float] = Field(
        sa_column=sa.Column(
            sa.DECIMAL,
            nullable=True,
        ),
    )


class LeaderboardOverall(SQLModel, table=True):
    __tablename__ = "leaderboard_overall"

    id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            primary_key=True,
            server_default=(sa.text("uuid_generate_v4()")),
        ),
    )
    user_id: UUID = Field(
        sa_column=sa.Column(
            sa_psql.UUID(as_uuid=True),
            nullable=False,
        ),
    )
    username: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        ),
    )
    languages: List[str] = Field(
        sa_column=sa.Column(
            sa.ARRAY(sa.Text),
        ),
        # NOTE: this is nullable temporarily while
        # we don't have to backfill leaderboard data yet
        nullable=True,
    )
    image_url: str = Field(
        sa_column=sa.Column(
            sa.Text,
            nullable=False,
        ),
    )
    rank: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )
    points: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )
    blended_rank: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )
    blended_points: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            nullable=False,
        ),
    )
    quality_score: Optional[float] = Field(
        sa_column=sa.Column(
            sa.DECIMAL,
            nullable=True,
        ),
    )

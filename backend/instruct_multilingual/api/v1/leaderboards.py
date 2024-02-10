import logging
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from instruct_multilingual import db
from instruct_multilingual.models import (
    LeaderboardDaily,
    LeaderboardWeekly,
    LeaderboardByLanguage,
    LeaderboardOverall,
)
from instruct_multilingual.schemas.leaderboard import (
    LeaderboardRecordList,
    OverallLeaderboardRecordList,
    LanguageLeaderboardRecordList,
)
from instruct_multilingual.exceptions import InstructMultilingualAPIError

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

router = APIRouter()


@router.get(
    "/daily/{user_id}/{day}",
    response_model=LeaderboardRecordList,
    status_code=status.HTTP_200_OK,
)
def get_leaderboard_daily(
    *,
    user_id: UUID,
    day: str,
):
    """
    Returns the current daily leaderboard.
    """
    logger.info(f"Retrieving daily leaderboard for {day}...")

    try:
        with Session(db.engine) as session:
            stmt = (
                select(LeaderboardDaily)
                .where(LeaderboardDaily.day == day)
                .order_by(LeaderboardDaily.rank)
            )
            result = session.exec(stmt)
            daily_leaderboard = result.fetchall()
    except Exception as e:
        logger.error(f"error retrieving daily leaderboard: {e}")
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error retrieving daily leaderboard",
        ) from e

    logger.debug(f"retrieved daily leaderboard: {daily_leaderboard}")

    if not daily_leaderboard:
        return LeaderboardRecordList(
            records=[],
            current_user=None,
        )

    current_user = None
    for record in daily_leaderboard:
        if record.user_id == user_id:
            current_user = record
            break

    return LeaderboardRecordList(
        records=daily_leaderboard,
        current_user=current_user,
    )


@router.get(
    "/weekly/{user_id}/{week_of}",
    response_model=LeaderboardRecordList,
    status_code=status.HTTP_200_OK,
)
def get_leaderboard_weekly(
    *,
    user_id: UUID,
    week_of: str,
):
    """
    Returns the current weekly leaderboard.
    """
    try:
        with Session(db.engine) as session:
            stmt = (
                select(LeaderboardWeekly)
                .where(LeaderboardWeekly.week_of == week_of)
                .order_by(LeaderboardWeekly.rank)
            )
            result = session.exec(stmt)
            weekly_leaderboard = result.fetchall()
    except Exception as e:
        logger.error(f"error retrieving weekly leaderboard: {e}")
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error retrieving weekly leaderboard",
        ) from e

    logger.debug(f"retrieved weekly leaderboard: {weekly_leaderboard}")

    if not weekly_leaderboard:
        return LeaderboardRecordList(
            records=[],
            current_user=None,
        )

    current_user = None
    for record in weekly_leaderboard:
        if record.user_id == user_id:
            current_user = record
            break

    return LeaderboardRecordList(
        records=weekly_leaderboard,
        current_user=current_user,
    )


@router.get(
    "/language/{user_id}/{language}",
    response_model=LanguageLeaderboardRecordList,
    status_code=status.HTTP_200_OK,
)
def get_leaderboard_by_language(
    *,
    user_id: UUID,
    language: str,
    order_by: str = "blended_rank",
):
    """
    Returns the current leaderboard based on the indicated language.
    """
    if order_by not in ["rank", "blended_rank"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"invalid order_by value: {order_by}. "
                "options are 'rank' or 'blended_rank'",
            ),
        )
    elif order_by == "rank":
        order_by = LeaderboardByLanguage.rank
    elif order_by == "blended_rank":
        order_by = LeaderboardByLanguage.blended_rank

    try:
        with Session(db.engine) as session:
            stmt = (
                select(LeaderboardByLanguage)
                .where(LeaderboardByLanguage.language_code == language)
                .order_by(order_by)
            )
            result = session.exec(stmt)
            language_leaderboard = result.fetchall()
    except Exception as e:
        logger.error(f"error retrieving language leaderboard: {e}")
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error retrieving language leaderboard",
        ) from e

    logger.debug(f"retrieved language leaderboard: {language_leaderboard}")

    if not language_leaderboard:
        return LanguageLeaderboardRecordList(
            records=[],
            current_user=None,
        )

    current_user = None
    for record in language_leaderboard:
        if record.user_id == user_id:
            current_user = record
            break

    return LanguageLeaderboardRecordList(
        records=language_leaderboard,
        current_user=current_user,
    )


@router.get(
    "/{user_id}/overall",
    response_model=OverallLeaderboardRecordList,
    status_code=status.HTTP_200_OK,
)
def get_leaderboard_overall(
    *,
    user_id: UUID,
    limit: int = 20,
    offset: int = 0,
    order_by: str = "blended_rank",
):
    """
    Returns the current leaderboard overall (since the beginning of time).
    """
    if order_by not in ["rank", "blended_rank"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"invalid order_by value: {order_by}. "
                "options are 'rank' or 'blended_rank'",
            ),
        )
    elif order_by == "rank":
        order_by = LeaderboardOverall.rank
    elif order_by == "blended_rank":
        order_by = LeaderboardOverall.blended_rank

    try:
        with Session(db.engine) as session:
            # get the top `limit` records, offset by `offset`
            stmt = select(
                LeaderboardOverall,
            ).order_by(
                order_by,
            ).limit(
                limit,
            ).offset(
                offset,
            )
            result = session.exec(stmt)
            overall_leaderboard = result.fetchall()

            total_count = session.query(LeaderboardOverall).count()

            # get the rank of the current user as well
            stmt = select(LeaderboardOverall).where(LeaderboardOverall.user_id == user_id)
            result = session.exec(stmt)

            current_user = result.first()
    except Exception as e:
        logger.error(f"error retrieving overall leaderboard: {e}")
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="error retrieving overall leaderboard",
        ) from e

    logger.debug(f"retrieved overall leaderboard: {overall_leaderboard}")

    if not overall_leaderboard:
        return OverallLeaderboardRecordList(
            records=[],
            current_user=None,
        )

    return OverallLeaderboardRecordList(
        records=overall_leaderboard,
        current_user=current_user,
        total_count=total_count,
    )

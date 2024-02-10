import logging

from datetime import datetime

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert

from sqlmodel import Session

from instruct_multilingual import db
from instruct_multilingual.models import (
    LeaderboardDaily,
)

from jobs.common import even_out_ranks, update_ranks_within_language_groups

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

def update_leaderboard_daily():
    """
    Query the task_audit and user table, and then update the `leaderboard_daily` table
    with the number of points each user has earned in the past day.

    Each task audit submitted is worth 2 points. Each user also gets a rank based
    on the number of points they have earned.

    The daily leaderboard is updated every 24 hours at 00:30 UTC, or otherwise
    determined by the Cloud Run job schedule.
    """
    query = """
    SELECT
        user_id,
        username,
        ARRAY_AGG(DISTINCT language) AS languages,
        SUM(points)                  AS points,
        lb_day,
        image_url,
        0 AS rank
    FROM (
        SELECT
            user_id,
            username,
            language,
            points,
            lb_day,
            image_url
        FROM (
            SELECT
                u.id                         AS user_id,
                u.username                   AS username,
                lc.name                      AS language,
                COALESCE(SUM(
                    CASE
                        WHEN ta.prompt_rating IS NOT NULL AND ta.completion_rating IS NOT NULL THEN 1
                        ELSE 0
                    END
                ), 0) +
                COALESCE(SUM(
                    CASE
                        WHEN ta.prompt_edited THEN 1
                        ELSE 0
                    END
                ), 0) +
                COALESCE(SUM(
                    CASE
                        WHEN ta.completion_edited THEN 1
                        ELSE 0
                    END
                ), 0) AS points,
                CURRENT_DATE                 AS lb_day,
                u.image_url                  AS image_url
            FROM
                task_audit ta
            INNER JOIN "user" u ON ta.submitted_by = u.id
            INNER JOIN task t ON ta.task_id = t.id
            INNER JOIN language_code lc ON t.language_id = lc.id
            WHERE
                -- current leaderboard represents the previous day
                -- so we need to subtract 1 day from the current date
                -- to account for all the tasks submitted.
                DATE_TRUNC('day', ta.created_at) = CURRENT_DATE
            GROUP BY
                u.id,
                lc.name,
                u.username,
                u.image_url

            UNION ALL

            SELECT
                u.id                        AS user_id,
                u.username                  AS username,
                lc.name                     AS language,
                COALESCE(SUM(2), 0)         AS points,
                CURRENT_DATE                AS lb_day,
                u.image_url                 AS image_url
            FROM
                task_contribution tc
            INNER JOIN "user" u ON tc.submitted_by = u.id
            INNER JOIN language_code lc ON tc.language_id = lc.id
            WHERE
                -- current leaderboard represents the previous day
                -- so we need to subtract 1 day from the current date
                -- to account for all the tasks submitted.
                DATE_TRUNC('day', tc.created_at) = CURRENT_DATE
            GROUP BY
                u.id,
                lc.name,
                u.username,
                u.image_url

            UNION ALL

            SELECT
                u.id                AS user_id,
                u.username          AS username,
                lc.name             AS language,
                COALESCE(SUM(
                    CASE
                        WHEN tca.prompt_rating IS NOT NULL AND tca.completion_rating IS NOT NULL THEN 1
                        ELSE 0
                    END
                ), 0) +
                COALESCE(SUM(
                    CASE
                        WHEN tca.prompt_edited THEN 1
                        ELSE 0
                    END
                ), 0) +
                COALESCE(SUM(
                    CASE
                        WHEN tca.completion_edited THEN 1
                        ELSE 0
                    END
                ), 0) AS points,
                CURRENT_DATE        AS lb_day,
                u.image_url         AS image_url
            FROM
                task_contribution_audit tca
            INNER JOIN "user" u ON tca.submitted_by = u.id
            INNER JOIN task_contribution tc ON tca.task_contribution_id = tc.id
            INNER JOIN language_code lc ON tc.language_id = lc.id
            WHERE
                -- current leaderboard represents the previous day
                -- so we need to subtract 1 day from the current date
                -- to account for all the tasks submitted.
                DATE_TRUNC('day', tca.created_at) = CURRENT_DATE
            GROUP BY
                u.id,
                lc.name,
                u.username,
                u.image_url

            UNION ALL

            SELECT
                u.id AS user_id,
                u.username AS username,
                lc.name AS language,
                COALESCE(SUM(
                    CASE
                        WHEN tar.edited_prompt_rating IS NOT NULL AND tar.edited_completion_rating IS NOT NULL THEN 1
                        ELSE 0
                    END
                ), 0) +
                COALESCE(SUM(
                    CASE
                        WHEN tar.improved_prompt IS NOT NULL THEN 1
                        ELSE 0
                    END
                ), 0) +
                COALESCE(SUM(
                    CASE
                        WHEN tar.improved_completion IS NOT NULL THEN 1
                        ELSE 0
                    END
                ), 0) AS points,
                CURRENT_DATE        AS lb_day,
                u.image_url AS image_url
            FROM
                task_audit_review tar
            INNER JOIN "user" u ON tar.submitted_by = u.id
            INNER JOIN task_audit ta ON tar.task_audit_id = ta.id
            INNER JOIN task t ON ta.task_id = t.id
            INNER JOIN language_code lc ON t.language_id = lc.id
            WHERE
                DATE_TRUNC('day', tar.created_at) = CURRENT_DATE
            GROUP BY
                u.id,
                lc.name,
                u.username,
                u.image_url

            UNION ALL

            SELECT
                u.id AS user_id,
                u.username AS username,
                lc.name AS language,
                COALESCE(SUM(
                    CASE
                        WHEN tcar.edited_prompt_rating IS NOT NULL AND tcar.edited_completion_rating IS NOT NULL THEN 1
                        ELSE 0
                    END
                ), 0) +
                COALESCE(SUM(
                    CASE
                        WHEN tcar.improved_prompt IS NOT NULL THEN 1
                        ELSE 0
                    END
                ), 0) +
                COALESCE(SUM(
                    CASE
                        WHEN tcar.improved_completion IS NOT NULL THEN 1
                        ELSE 0
                    END
                ), 0) AS points,
                CURRENT_DATE        AS lb_day,
                u.image_url AS image_url
            FROM
                task_contribution_audit_review tcar
            INNER JOIN "user" u ON tcar.submitted_by = u.id
            INNER JOIN task_contribution_audit tca ON tcar.task_contribution_audit_id = tca.id
            INNER JOIN task_contribution tc ON tca.task_contribution_id = tc.id
            INNER JOIN language_code lc ON tc.language_id = lc.id
            WHERE
                DATE_TRUNC('day', tcar.created_at) = CURRENT_DATE
            GROUP BY
                u.id,
                lc.name,
                u.username,
                u.image_url

        ) AS combined_results
    ) AS final_results
    GROUP BY
        user_id,
        username,
        image_url,
        lb_day
    ORDER BY
        points DESC;
    """

    logger.info(f'updating daily leaderboard for date {datetime.utcnow().date()}...')
    try:
        with Session(db.engine) as session:
            # get the daily records by combining the user table and the task_audit table
            daily_records = session.execute(text(query)).all()

            if not daily_records:
                logger.info('no records found for daily leaderboard update')
                return None

            # then re-rank the users based on the number of points they have earned
            # in the past 24 hours
            daily_records.sort(key=lambda x: x.points, reverse=True)

            # create a list of LeaderboardDaily objects and then assign them a rank
            # based on their position in the sorted list
            daily_leaderboard_records = []
            for i, record in enumerate(daily_records):
                lb_record = dict(
                    user_id=record.user_id,
                    username=record.username,
                    languages=record.languages,
                    points=record.points,
                    day=record.lb_day,
                    image_url=record.image_url,
                    rank=i+1,
                )
                daily_leaderboard_records.append(lb_record)

            daily_leaderboard_records = even_out_ranks(daily_leaderboard_records)

            # then update the daily leaderboard table
            insert_stmt = insert(
                LeaderboardDaily
            ).values(
                daily_leaderboard_records
            )

            statement = insert_stmt.on_conflict_do_update(
                index_elements=['user_id', 'day'],
                # update the points and rank columns
                # if the user_id and day already exist in the table
                set_={
                    'points': insert_stmt.excluded.points,
                    'rank': insert_stmt.excluded.rank,
                    'languages': insert_stmt.excluded.languages,
                    'username': insert_stmt.excluded.username,
                },
            ).returning(
                LeaderboardDaily.id
            )
            results = session.execute(statement).fetchall()
            session.commit()
    except Exception as e:
        logger.error(f'error while updating daily leaderboard: {e}')
        raise e
    else:
        logger.info(f'daily leaderboard updated for date {datetime.utcnow().date()} with {len(results)} records!')
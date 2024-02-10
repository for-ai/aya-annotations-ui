import logging

from datetime import datetime, timedelta

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert

from sqlmodel import Session

from instruct_multilingual import db
from instruct_multilingual.models import (
    LeaderboardWeekly,
)

from jobs.common import even_out_ranks, update_ranks_within_language_groups

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)


def update_leaderboard_weekly():
    """
    Query the task_audit and user table, and then update the `leaderboard_daily` table
    with the number of points each user has earned in the past week.
    """
    query = """
    -- combined task audit and task contribution points using UNION ALL
    SELECT
        user_id,
        username,
        ARRAY_AGG(DISTINCT language) AS languages,
        SUM(points) AS points,
        lb_week,
        image_url,
        0 AS rank
    FROM (
        SELECT
            user_id,
            username,
            language,
            points,
            lb_week,
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
                DATE_TRUNC(
                    'week',
                    CURRENT_DATE
                )                            AS lb_week,
                u.image_url                  AS image_url
            FROM
                task_audit ta
            INNER JOIN "user" u ON ta.submitted_by = u.id
            INNER JOIN task t ON ta.task_id = t.id
            INNER JOIN language_code lc ON t.language_id = lc.id
            WHERE
                -- Find records that begin on Monday and end on Sunday at 23:59 UTC
                ta.created_at >= DATE_TRUNC('week', CURRENT_DATE)
            AND
                ta.created_at < DATE_TRUNC('week', CURRENT_DATE) + INTERVAL '1 week'
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
                DATE_TRUNC(
                    'week',
                    CURRENT_DATE
                )                           AS lb_week,
                u.image_url                 AS image_url
            FROM
                task_contribution tc
            INNER JOIN "user" u ON tc.submitted_by = u.id
            INNER JOIN language_code lc ON tc.language_id = lc.id
            WHERE
                -- Find records that begin on Monday and end on Sunday at 23:59 UTC
                tc.created_at >= DATE_TRUNC('week', CURRENT_DATE)
            AND
                tc.created_at < DATE_TRUNC('week', CURRENT_DATE) + INTERVAL '1 week'
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
                DATE_TRUNC(
                    'week',
                    CURRENT_DATE
                )                   AS lb_week,
                u.image_url         AS image_url
            FROM
                task_contribution_audit tca
            INNER JOIN "user" u ON tca.submitted_by = u.id
            INNER JOIN task_contribution tc ON tca.task_contribution_id = tc.id
            INNER JOIN language_code lc ON tc.language_id = lc.id
            WHERE
                -- Find records that begin on Monday and end on Sunday at 23:59 UTC
                tc.created_at >= DATE_TRUNC('week', CURRENT_DATE)
            AND
                tc.created_at < DATE_TRUNC('week', CURRENT_DATE) + INTERVAL '1 week'
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
                DATE_TRUNC(
                    'week',
                    CURRENT_DATE
                )                   AS lb_week,
                u.image_url AS image_url
            FROM
                task_audit_review tar
            INNER JOIN "user" u ON tar.submitted_by = u.id
            INNER JOIN task_audit ta ON tar.task_audit_id = ta.id
            INNER JOIN task t ON ta.task_id = t.id
            INNER JOIN language_code lc ON t.language_id = lc.id
            WHERE
                -- Find records that begin on Monday and end on Sunday at 23:59 UTC
                tar.created_at >= DATE_TRUNC('week', CURRENT_DATE)
            AND
                tar.created_at < DATE_TRUNC('week', CURRENT_DATE) + INTERVAL '1 week'
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
                DATE_TRUNC(
                    'week',
                    CURRENT_DATE
                )                   AS lb_week,
                u.image_url AS image_url
            FROM
                task_contribution_audit_review tcar
            INNER JOIN "user" u ON tcar.submitted_by = u.id
            INNER JOIN task_contribution_audit tca ON tcar.task_contribution_audit_id = tca.id
            INNER JOIN task_contribution tc ON tca.task_contribution_id = tc.id
            INNER JOIN language_code lc ON tc.language_id = lc.id
            WHERE
                -- Find records that begin on Monday and end on Sunday at 23:59 UTC
                tcar.created_at >= DATE_TRUNC('week', CURRENT_DATE)
            AND
                tcar.created_at < DATE_TRUNC('week', CURRENT_DATE) + INTERVAL '1 week'
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
        lb_week
    ORDER BY
        points DESC;
    """
    # Get the current date
    today = datetime.utcnow().date()

    # Calculate the start of the week (Monday)
    start_of_week = today - timedelta(days=today.weekday())

    logger.info(f'updating weekly leaderboard for week of {start_of_week}...')
    try:
        with Session(db.engine) as session:
            # get the weekly records by combining the user table and the task_audit table
            weekly_records = session.execute(text(query)).all()

            if not weekly_records:
                logger.info('no records found for weekly leaderboard update')
                return None

            # then re-rank the users based on the number of points they have earned
            # in the past 7 days
            weekly_records.sort(key=lambda x: x.points, reverse=True)

            # create a list of LeaderboardWeekly objects and then assign them a rank
            # based on their position in the sorted list
            weekly_leaderboard_records = []
            for i, record in enumerate(weekly_records):
                lb_record = dict(
                    user_id=record.user_id,
                    username=record.username,
                    languages=record.languages,
                    points=record.points,
                    week_of=record.lb_week,
                    image_url=record.image_url,
                    rank=i+1,
                )
                weekly_leaderboard_records.append(lb_record)

            weekly_leaderboard_records = even_out_ranks(weekly_leaderboard_records)

            # then update the weekly leaderboard table
            insert_stmt = insert(
                LeaderboardWeekly
            ).values(
                weekly_leaderboard_records
            )

            statement = insert_stmt.on_conflict_do_update(
                index_elements=['user_id', 'week_of'],
                # update the points and rank columns
                # if the user_id and week already exist in the table
                set_={
                    'points': insert_stmt.excluded.points,
                    'username': insert_stmt.excluded.username,
                    'rank': insert_stmt.excluded.rank,
                    'languages': insert_stmt.excluded.languages,
                },
            ).returning(
                LeaderboardWeekly.id
            )
            results = session.execute(statement).fetchall()
            session.commit()
    except Exception as e:
        logger.error(f'error while updating weekly leaderboard: {e}')
        raise e
    else:
        logger.info(f'weekly leaderboard updated for week of {start_of_week} with {len(results)} records!')
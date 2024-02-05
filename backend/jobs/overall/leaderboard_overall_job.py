import logging

from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert

from sqlmodel import Session

from instruct_multilingual import db
from instruct_multilingual.models import (
    LeaderboardOverall,
)

from jobs.common import (
    compute_aya_score,
    even_out_ranks,
    even_out_blended_ranks,
    update_ranks_within_language_groups,
)


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)


def update_leaderboard_overall():
    """
    Query the task_audit and user table, and then update the `leaderboard_overall` table.
    """
    logger.info('updating overall leaderboard...')

    query = """
    -- combined task audit and task contribution points using UNION ALL
    SELECT
        user_id,
        username,
        ARRAY_AGG(DISTINCT language) AS languages,
        SUM(points)                  AS points,
        image_url,
        0 AS rank,
        0 AS blended_rank
    FROM (
        SELECT
            user_id,
            username,
            language,
            points,
            image_url
        FROM (
            SELECT
                u.id AS user_id,
                u.username AS username,
                lc.name AS language,
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
                u.image_url AS image_url
            FROM
                task_audit ta
            INNER JOIN "user" u ON ta.submitted_by = u.id
            INNER JOIN task t ON ta.task_id = t.id
            INNER JOIN language_code lc ON t.language_id = lc.id
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
                COALESCE(SUM(2), 0) AS points,
                u.image_url AS image_url
            FROM
                task_contribution tc
            INNER JOIN "user" u ON tc.submitted_by = u.id
            INNER JOIN language_code lc ON tc.language_id = lc.id
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
                u.image_url AS image_url
            FROM
                task_contribution_audit tca
            INNER JOIN "user" u ON tca.submitted_by = u.id
            INNER JOIN task_contribution tc ON tca.task_contribution_id = tc.id
            INNER JOIN language_code lc ON tc.language_id = lc.id
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
                u.image_url AS image_url
            FROM
                task_audit_review tar
            INNER JOIN "user" u ON tar.submitted_by = u.id
            INNER JOIN task_audit ta ON tar.task_audit_id = ta.id
            INNER JOIN task t ON ta.task_id = t.id
            INNER JOIN language_code lc ON t.language_id = lc.id
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
                u.image_url AS image_url
            FROM
                task_contribution_audit_review tcar
            INNER JOIN "user" u ON tcar.submitted_by = u.id
            INNER JOIN task_contribution_audit tca ON tcar.task_contribution_audit_id = tca.id
            INNER JOIN task_contribution tc ON tca.task_contribution_id = tc.id
            INNER JOIN language_code lc ON tc.language_id = lc.id
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
        image_url
    ORDER BY
        points DESC;
    """

    # first, we'll update the overall leaderboard table with points and ranks
    try:
        with Session(db.engine) as session:
            # get the records by combining the user table and the task_audit table
            overall_records = session.execute(text(query)).all()

            if not overall_records:
                logger.info('no records found for overall leaderboard update')
                return None

            # then re-rank the users based on the number of points they have earned
            # overall
            overall_records.sort(key=lambda x: x.points, reverse=True)

            # create a list of LeaderboardOverall objects and then assign them a rank
            # based on their position in the sorted list
            overall_leaderboard_records = []
            for i, record in enumerate(overall_records):
                lb_record = dict(
                    user_id=record.user_id,
                    languages=record.languages,
                    username=record.username,
                    points=record.points,
                    image_url=record.image_url,
                    rank=i+1,
                )
                overall_leaderboard_records.append(lb_record)

            overall_leaderboard_records = even_out_ranks(overall_leaderboard_records)

            # then update the leaderboard_overall table
            insert_stmt = insert(
                LeaderboardOverall
            ).values(
                overall_leaderboard_records
            )

            statement = insert_stmt.on_conflict_do_update(
                index_elements=['user_id'],
                # update the points and rank columns
                # if the user_id already exists in the table
                set_={
                    'points': insert_stmt.excluded.points,
                    'rank': insert_stmt.excluded.rank,
                    'languages': insert_stmt.excluded.languages,
                    'username': insert_stmt.excluded.username,
                },
            ).returning(
                LeaderboardOverall.id
            )
            results = session.execute(statement).fetchall()
            session.commit()
    except Exception as e:
        logger.error(f'error while updating overall leaderboard: {e}')
        raise e
    else:
        logger.info(f'overall leaderboard updated with {len(results)} records!')

    # next we'll use the existing records in the leaderboard_overall table to
    # update the blended points and blended ranks
    quality_score_query = """
    -- Calculate the average rating for each user based on the reviews they have received for task audits
    WITH combined_task_audit_reviews AS (
        SELECT
            u.id AS user_id,
            u.username AS username,
            AVG((tar.edited_prompt_rating + tar.edited_completion_rating) / 2) AS avg_rating_for_task_audits
        FROM task_audit_review tar
        JOIN task_audit ta ON ta.id = tar.task_audit_id
        JOIN "user" u ON u.id = ta.submitted_by
        GROUP BY u.id, u.username

        UNION ALL

        SELECT
            u.id AS user_id,
            u.username AS username,
            AVG((tcar.edited_prompt_rating + tcar.edited_completion_rating) / 2) AS avg_rating_for_task_audits
        FROM task_contribution_audit_review tcar
        JOIN task_contribution_audit tca ON tca.id = tcar.task_contribution_audit_id
        JOIN "user" u ON u.id = tca.submitted_by
        GROUP BY u.id, u.username
    ),
    -- Calculate the number of audits each user has completed and also edited
    task_audits_edited AS (
        SELECT
            u.id AS user_id,
            u.username AS username,
            SUM(
                CASE
                    WHEN (ta.prompt_edited = true OR ta.completion_edited = true) THEN 1
                    ELSE 0
                END
            ) AS num_audits_edited
        FROM task_audit ta
        JOIN "user" u ON u.id = ta.submitted_by
        GROUP BY u.id, u.username

        UNION ALL

        SELECT
            u.id AS user_id,
            u.username AS username,
            SUM(
                CASE
                    WHEN (tca.prompt_edited = true OR tca.completion_edited = true) THEN 1
                    ELSE 0
                END
            ) AS num_audits_edited
        FROM task_contribution_audit tca
        JOIN "user" u ON u.id = tca.submitted_by
        GROUP BY u.id, u.username
    ),
    -- this counts the number of audits each user has reviewed in task 3
    -- and further edited
    task_audits_reviewed AS (
        SELECT
            u.id AS user_id,
            u.username AS username,
            COUNT(*) AS num_audits_reviewed_and_improved
        FROM task_audit_review tar
        JOIN "user" u ON u.id = tar.submitted_by
        WHERE (tar.improved_prompt != '' OR tar.improved_completion != '')
        GROUP BY u.id, u.username

        UNION ALL

        SELECT
            u.id AS user_id,
            u.username AS username,
            COUNT(*) AS num_audits_reviewed_and_improved
        FROM task_contribution_audit_review tcar
        JOIN "user" u ON u.id = tcar.submitted_by
        WHERE (tcar.improved_prompt != '' OR tcar.improved_completion != '')
        GROUP BY u.id, u.username
    ),
    -- count the number of tasks that have been contributed per user
    tasks_contributed AS (
        SELECT
            u.id as user_id,
            u.username,
            COUNT(*) as num_tasks_contributed
        FROM task_contribution tc
        JOIN "user" u ON u.id = tc.submitted_by
        GROUP BY u.id, u.username
        ORDER BY u.username ASC
    ),
    -- count the number of thumbs up out of total audits given per user
    task_audits_for_contributions AS (
        SELECT
            u.id AS user_id,
            u.username,
            tc.id AS task_contribution_id,
            tca.prompt_rating,
            tca.completion_rating
        FROM public."user" u
        JOIN task_contribution tc ON u.id = tc.submitted_by
        JOIN task_contribution_audit tca ON tc.id = tca.task_contribution_id
    ),
    thumbs_up_per_contribution_audit AS (
        SELECT
            user_id,
            username,
            COUNT(DISTINCT task_contribution_id) AS total_contributions,
            COUNT(*) AS total_audits,
            SUM(CASE WHEN prompt_rating = 1 THEN 1 ELSE 0 END) AS positive_prompt_ratings,
            SUM(CASE WHEN completion_rating = 1 THEN 1 ELSE 0 END) AS positive_completion_ratings
        FROM task_audits_for_contributions
        GROUP BY user_id, username
    ),
    thumbs_up_ratio_per_contribution_audit AS (
        SELECT
            user_id,
            username,
            CASE WHEN total_audits > 0 THEN (positive_prompt_ratings::decimal / total_audits) ELSE 0.0 END AS avg_prompt_thumbs_up_ratio,
            CASE WHEN total_audits > 0 THEN (positive_completion_ratings::decimal / total_audits) ELSE 0.0 END AS avg_completion_thumbs_up_ratio,
            CASE WHEN total_audits > 0 THEN ((positive_prompt_ratings::decimal / total_audits) + (positive_completion_ratings::decimal / total_audits)) / 2 ELSE 0.0 END AS avg_thumbs_up_ratio
        FROM thumbs_up_per_contribution_audit
    ),
    aggregated_user_data AS (
        SELECT
            u.id AS user_id,
            u.username AS username,
            COALESCE(AVG(ctar.avg_rating_for_task_audits), 0) AS avg_quality_score,
            COALESCE(SUM(e.num_audits_edited), 0) AS num_audits_edited,
            COALESCE(SUM(r.num_audits_reviewed_and_improved), 0) AS num_audits_reviewed_and_improved,
            t.num_tasks_contributed AS num_tasks_contributed
        FROM "user" u
        LEFT JOIN task_audits_edited e ON u.id = e.user_id
        LEFT JOIN task_audits_reviewed r ON u.id = r.user_id
        LEFT JOIN tasks_contributed t ON u.id = t.user_id
        LEFT JOIN combined_task_audit_reviews ctar ON u.id = ctar.user_id
        GROUP BY u.id, u.username, t.num_tasks_contributed
    )
    -- Combine and join the aggregated user data with the other subqueries
    SELECT
        u.id AS user_id,
        u.username AS username,
        COALESCE(a.avg_quality_score, 0) AS avg_quality_score,
        COALESCE(a.num_audits_edited, 0) AS num_audits_edited,
        COALESCE(a.num_audits_reviewed_and_improved, 0) AS num_audits_reviewed_and_improved,
        COALESCE(a.num_tasks_contributed, 0) AS num_tasks_contributed,
        COALESCE(tp.avg_thumbs_up_ratio, 0) AS avg_thumbs_up_ratio
    FROM "user" u
    LEFT JOIN aggregated_user_data a ON u.id = a.user_id
    LEFT JOIN thumbs_up_ratio_per_contribution_audit tp ON u.id = tp.user_id
    ORDER BY username ASC;
    """
    try:
        with Session(db.engine) as session:
            # get the records by combining the user table and the task_audit table
            aya_score_component_records = session.execute(text(quality_score_query)).all()

            if not aya_score_component_records:
                raise Exception('no records found for quality score update')

            # create a list of user_ids for users we computed scores for
            aya_score_user_ids = [
                record.user_id
                for record in aya_score_component_records
            ]

            # then get the records from the leaderboard_overall table
            leaderboard_records = session.query(LeaderboardOverall).all()

            # then assign blended points to each user based on the function:
            # Aya Score = AYA Score = max(0, (Avg Quality - 3.0)) *
            # (3.0 * (Number Prompts / Completions Audited and Edited + Number of Tasks Further Edited)) +
            # ( 3.0 * (Number of Thumbs Up / Number of Thumbs) * Number of Task 2 Contributions )
            # where Quality is the average rating for the user.
            #
            # We are essentially extrapolating out the average score computed in task 3 to
            # everything the user has audited and edited. Which makes sense because we are essentially
            # saying we form a guess of quality based on a subset but reward the user for all edits
            # they have done as a sign since we trust the sample edited is a good proxy for overall quality.
            for lb_record in leaderboard_records:
                if lb_record.user_id in aya_score_user_ids:
                    for record in aya_score_component_records:
                        if record.user_id == lb_record.user_id:
                            logger.info(
                                'computing aya score for user_id and username: '
                                f'{lb_record.user_id}, {lb_record.username}'
                            )
                            aya_score = compute_aya_score(
                                thumbs_up_received_ratio=record.avg_thumbs_up_ratio,
                                num_contributed_tasks=record.num_tasks_contributed,
                                avg_quality_score=record.avg_quality_score,
                                num_audits_edited=record.num_audits_edited,
                                num_audits_further_improved=record.num_audits_reviewed_and_improved,
                            )
                            lb_record.blended_points = round(aya_score)
                            lb_record.quality_score = round(record.avg_quality_score, 2)
                else:
                    # this should never happen
                    logger.error('no aya score found for user_id: {lb_record.user_id} and username: {lb_record.username}')
                    raise Exception('no aya score found for user_id: {lb_record.user_id} and username: {lb_record.username}')

            # then re-rank the users based on the number of blended points they have earned
            leaderboard_records.sort(key=lambda x: x.blended_points, reverse=True)

            # assign a blended rank based on their position in the sorted list
            for i, record in enumerate(leaderboard_records):
                record.blended_rank = i+1

            # if any users have the same number of blended points, then they should
            # have the same blended rank
            leaderboard_records = even_out_blended_ranks(leaderboard_records)

            # then commit the changes to the database
            session.commit()
    except Exception as e:
        logger.error(f'error while updating blended ranking and points for overall leaderboard: {e}')
        raise e
    else:
        logger.info('blended ranking and points updated for overall leaderboard!')

import logging

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert

from sqlmodel import Session

from instruct_multilingual import db
from instruct_multilingual.models import (
    LeaderboardByLanguage,
)

from jobs.common import (
    compute_aya_score,
    even_out_ranks,
    even_out_blended_ranks,
    update_blended_ranks_within_language_groups,
    update_ranks_within_language_groups,
)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)


def update_leaderboard_by_language():
    """
    Query the task_audit, language_code, task, and user table, and then update the `leaderboard_by_language` table
    with the number of points each user has earned overall.
    """
    logger.info('updating leaderboard by language...')

    query = """
    -- combined task audit and task contribution points using UNION ALL
    SELECT
        user_id,
        username,
        language,
        language_code,
        SUM(points) AS points,
        image_url,
        0 AS rank
    FROM (
        SELECT
            user_id,
            username,
            language,
            language_code,
            points,
            image_url
        FROM (
            SELECT
                u.id                      AS user_id,
                u.username                AS username,
                lc.name                   AS language,
                lc.code                   AS language_code,
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
                u.image_url               AS image_url
            FROM
                task_audit ta
            INNER JOIN "user" u ON ta.submitted_by = u.id
            INNER JOIN task t ON ta.task_id = t.id
            INNER JOIN language_code lc ON t.language_id = lc.id
            GROUP BY
                u.id,
                lc.name,
                u.username,
                u.image_url,
                lc.code

            UNION ALL

            SELECT
                u.id                        AS user_id,
                u.username                  AS username,
                lc.name                     AS language,
                lc.code                     AS language_code,
                COALESCE(SUM(2), 0)         AS points,
                u.image_url                 AS image_url
            FROM
                task_contribution tc
            INNER JOIN "user" u ON tc.submitted_by = u.id
            INNER JOIN language_code lc ON tc.language_id = lc.id
            GROUP BY
                u.id,
                lc.name,
                u.username,
                u.image_url,
                lc.code

            UNION ALL

            SELECT
                u.id                AS user_id,
                u.username          AS username,
                lc.name             AS language,
                lc.code             AS language_code,
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
                u.image_url         AS image_url
            FROM
                task_contribution_audit tca
            INNER JOIN "user" u ON tca.submitted_by = u.id
            INNER JOIN task_contribution tc ON tca.task_contribution_id = tc.id
            INNER JOIN language_code lc ON tc.language_id = lc.id
            GROUP BY
                u.id,
                lc.name,
                u.username,
                u.image_url,
                lc.code

            UNION ALL

            SELECT
                u.id                AS user_id,
                u.username          AS username,
                lc.name             AS language,
                lc.code             AS language_code,
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
                u.image_url         AS image_url
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
                u.image_url,
                lc.code

            UNION ALL

            SELECT
                u.id                AS user_id,
                u.username          AS username,
                lc.name             AS language,
                lc.code             AS language_code,
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
                u.image_url         AS image_url
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
                u.image_url,
                lc.code

        ) AS combined_results
    ) AS final_results
    GROUP BY
        user_id,
        username,
        image_url,
        language,
        language_code
    ORDER BY
        points DESC;
    """

    try:
        with Session(db.engine) as session:
            # get the records by combining the user table and the task_audit table
            by_language_records = session.execute(text(query)).all()

            if not by_language_records:
                logger.info('no records found for leaderboard by language update')
                return None

            # then re-rank the users based on the number of points they have earned
            # overall
            by_language_records.sort(key=lambda x: x.points, reverse=True)

            # create a list of LeaderboardByLanguage objects and then assign them a rank
            # based on their position in the sorted list
            by_language_leaderboard_records = []
            for i, record in enumerate(by_language_records):
                lb_record = dict(
                    user_id=record.user_id,
                    username=record.username,
                    points=record.points,
                    language=record.language,
                    language_code=record.language_code,
                    image_url=record.image_url,
                    rank=i+1,
                )
                by_language_leaderboard_records.append(lb_record)

            # users should be ranked _within_ each language, and not overall
            logger.info('updating ranks within language groups...')
            by_language_leaderboard_records = update_ranks_within_language_groups(
                by_language_leaderboard_records,
            )
            logger.info('ranks within language groups updated!')

            # then update the leaderboard_by_language table
            insert_stmt = insert(
                LeaderboardByLanguage
            ).values(
                by_language_leaderboard_records
            )

            statement = insert_stmt.on_conflict_do_update(
                index_elements=['user_id', 'language'],
                # update the points and rank columns
                # if the user_id and language already exist in the table
                set_={
                    'points': insert_stmt.excluded.points,
                    'rank': insert_stmt.excluded.rank,
                    'username': insert_stmt.excluded.username,
                },
            ).returning(
                LeaderboardByLanguage.id
            )
            results = session.execute(statement).fetchall()
            session.commit()
    except Exception as e:
        logger.error(f'error while updating leaderboard by language: {e}')
        raise e
    else:
        logger.info(f'leaderboard by language updated with {len(results)} records!')

    # next we'll use the existing records in the leaderboard_by_language table to
    # update the blended points and blended ranks
    quality_score_query = """
    -- Calculate the average rating for each user and language they've contributed to based on the reviews they have received for task audits
    WITH combined_task_audit_reviews AS (
        SELECT
            u.id AS user_id,
            u.username AS username,
            lc.name AS language_name,
            AVG((tar.edited_prompt_rating + tar.edited_completion_rating) / 2) AS avg_rating_for_task_audits
        FROM task_audit_review tar
        JOIN task_audit ta ON ta.id = tar.task_audit_id
        JOIN "user" u ON u.id = ta.submitted_by
        JOIN task t on ta.task_id = t.id
        JOIN language_code lc ON lc.id = t.language_id
        GROUP BY u.id, u.username, lc.id

        UNION ALL

        SELECT
            u.id AS user_id,
            u.username AS username,
            lc.name AS language_name,
            AVG((tcar.edited_prompt_rating + tcar.edited_completion_rating) / 2) AS avg_rating_for_task_audits
        FROM task_contribution_audit_review tcar
        JOIN task_contribution_audit tca ON tca.id = tcar.task_contribution_audit_id
        JOIN task_contribution tc on tca.task_contribution_id = tc.id
        JOIN "user" u ON u.id = tca.submitted_by
        JOIN language_code lc ON lc.id = tc.language_id
        GROUP BY u.id, u.username, lc.id
    ),
    -- Calculate the number of audits each user and language they've contributed to has completed and also edited
    task_audits_edited AS (
        SELECT
            u.id AS user_id,
            u.username AS username,
            lc.name AS language_name,
            SUM(
                CASE
                    WHEN (ta.prompt_edited = true OR ta.completion_edited = true) THEN 1
                    ELSE 0
                END
            ) AS num_audits_edited
        FROM task_audit ta
        JOIN task t on ta.task_id = t.id
        JOIN "user" u ON u.id = ta.submitted_by
        JOIN language_code lc ON lc.id = t.language_id
        GROUP BY u.id, u.username, lc.id

        UNION ALL

        SELECT
            u.id AS user_id,
            u.username AS username,
            lc.name AS language_name,
            SUM(
                CASE
                    WHEN (tca.prompt_edited = true OR tca.completion_edited = true) THEN 1
                    ELSE 0
                END
            ) AS num_audits_edited
        FROM task_contribution_audit tca
        JOIN task_contribution tc on tca.task_contribution_id = tc.id
        JOIN "user" u ON u.id = tca.submitted_by
        JOIN language_code lc ON lc.id = tc.language_id
        GROUP BY u.id, u.username, lc.id
    ),
    -- This counts the number of audits each user and language they've contributed to has reviewed and further edited
    task_audits_reviewed AS (
        SELECT
            u.id AS user_id,
            u.username AS username,
            lc.name AS language_name,
            COUNT(*) AS num_audits_reviewed_and_improved
        FROM task_audit_review tar
        JOIN task_audit ta ON ta.id = tar.task_audit_id
        JOIN task t on ta.task_id = t.id
        JOIN "user" u ON u.id = tar.submitted_by
        JOIN language_code lc ON lc.id = t.language_id
        WHERE (tar.improved_prompt != '' OR tar.improved_completion != '')
        GROUP BY u.id, u.username, lc.id

        UNION ALL

        SELECT
            u.id AS user_id,
            u.username AS username,
            lc.name AS language_name,
            COUNT(*) AS num_audits_reviewed_and_improved
        FROM task_contribution_audit_review tcar
        JOIN task_contribution_audit tca ON tca.id = tcar.task_contribution_audit_id
        JOIN task_contribution tc on tca.task_contribution_id = tc.id
        JOIN "user" u ON u.id = tcar.submitted_by
        JOIN language_code lc ON lc.id = tc.language_id
        WHERE (tcar.improved_prompt != '' OR tcar.improved_completion != '')
        GROUP BY u.id, u.username, lc.id
    ),
    -- Count the number of tasks that have been contributed per user and language they've contributed to
    tasks_contributed AS (
        SELECT
            u.id as user_id,
            u.username,
            lc.name AS language_name,
            COUNT(*) as num_tasks_contributed
        FROM task_contribution tc
        JOIN "user" u ON u.id = tc.submitted_by
        JOIN language_code lc ON lc.id = tc.language_id
        GROUP BY u.id, u.username, lc.id
        ORDER BY u.username ASC
    ),
    -- Count the number of thumbs up out of total audits given per user and language they've contributed to
    task_audits_for_contributions AS (
        SELECT
            u.id AS user_id,
            u.username,
            lc.name AS language_name,
            tc.id AS task_contribution_id,
            tca.prompt_rating,
            tca.completion_rating
        FROM public."user" u
        JOIN task_contribution tc ON u.id = tc.submitted_by
        JOIN task_contribution_audit tca ON tc.id = tca.task_contribution_id
        JOIN language_code lc ON lc.id = tc.language_id
    ),
    thumbs_up_per_contribution_audit AS (
        SELECT
            user_id,
            username,
            language_name,
            COUNT(DISTINCT task_contribution_id) AS total_contributions,
            COUNT(*) AS total_audits,
            SUM(CASE WHEN prompt_rating = 1 THEN 1 ELSE 0 END) AS positive_prompt_ratings,
            SUM(CASE WHEN completion_rating = 1 THEN 1 ELSE 0 END) AS positive_completion_ratings
        FROM task_audits_for_contributions
        GROUP BY user_id, username, language_name
    ),
    thumbs_up_ratio_per_contribution_audit AS (
        SELECT
            user_id,
            username,
            language_name,
            CASE WHEN total_audits > 0 THEN (positive_prompt_ratings::decimal / total_audits) ELSE 0.0 END AS avg_prompt_thumbs_up_ratio,
            CASE WHEN total_audits > 0 THEN (positive_completion_ratings::decimal / total_audits) ELSE 0.0 END AS avg_completion_thumbs_up_ratio,
            CASE WHEN total_audits > 0 THEN ((positive_prompt_ratings::decimal / total_audits) + (positive_completion_ratings::decimal / total_audits)) / 2 ELSE 0.0 END AS avg_thumbs_up_ratio
        FROM thumbs_up_per_contribution_audit
    ),
    aggregated_user_data AS (
        SELECT
            u.id AS user_id,
            u.username AS username,
            lc.name AS language_name,
            COALESCE(AVG(ctar.avg_rating_for_task_audits), 0) AS avg_quality_score,
            COALESCE(SUM(e.num_audits_edited), 0) AS num_audits_edited,
            COALESCE(SUM(r.num_audits_reviewed_and_improved), 0) AS num_audits_reviewed_and_improved,
            COALESCE(t.num_tasks_contributed, 0) AS num_tasks_contributed
        FROM
            "user" u
            JOIN language_code lc ON lc.id = ANY(u.language_codes)
            LEFT JOIN combined_task_audit_reviews ctar ON u.id = ctar.user_id
                AND lc.name = ctar.language_name
            LEFT JOIN task_audits_edited e ON u.id = e.user_id
                AND lc.name = e.language_name
            LEFT JOIN task_audits_reviewed r ON u.id = r.user_id
                AND lc.name = r.language_name
            LEFT JOIN tasks_contributed t ON u.id = t.user_id
                AND lc.name = t.language_name
        GROUP BY
            u.id,
            u.username,
            lc.name,
            t.num_tasks_contributed
    )
    -- Combine and join the aggregated user data with the other subqueries
    SELECT
        agg.user_id AS user_id,
        agg.username AS username,
        agg.language_name AS language_name,
        COALESCE(agg.avg_quality_score, 0) AS avg_quality_score,
        COALESCE(agg.num_audits_edited, 0) AS num_audits_edited,
        COALESCE(agg.num_audits_reviewed_and_improved, 0) AS num_audits_reviewed_and_improved,
        COALESCE(agg.num_tasks_contributed, 0) AS num_tasks_contributed,
        COALESCE(tp.avg_thumbs_up_ratio, 0) AS avg_thumbs_up_ratio
    FROM
        aggregated_user_data agg
    LEFT JOIN thumbs_up_ratio_per_contribution_audit tp ON agg.user_id = tp.user_id
        AND agg.language_name = tp.language_name
    ORDER BY
        username ASC,
        language_name ASC;
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

            # then get the records from the leaderboard_by_language table
            leaderboard_records = session.query(LeaderboardByLanguage).all()

            # then assign blended points to each user based on the function:
            # Aya Score = AYA Score = max(0, (Avg Quality - 3.0)) *
            # (3.0 * (Number Prompts / Completions Audited and Edited + Number of Tasks Further Edited)) +
            # ( 3.0 * (Number of Thumbs Up / Number of Thumbs) * Number of Task 2 Contributions )
            # where Quality is the average rating for the user.
            #
            # We are essentially extrapolating out the average score computed in task 3 to
            # everything the user has audited and edited. Which makes sense because we are essentially
            # saying we form a guess of quality based on a subset but reward the user for all edits
            # they have done as a sign since we trust the sample edited is a good proxy for by_language quality.
            #
            # These aya scores below are specific to each language a user has contributed to.
            for lb_record in leaderboard_records:
                if lb_record.user_id in aya_score_user_ids:
                    for record in aya_score_component_records:
                        if record.user_id == lb_record.user_id and record.language_name == lb_record.language:
                            logger.debug(
                                'computing aya score for user_id, username, and language: '
                                f'{lb_record.user_id}, {lb_record.username}, {lb_record.language}'
                            )
                            aya_score_for_language = compute_aya_score(
                                thumbs_up_received_ratio=record.avg_thumbs_up_ratio,
                                num_contributed_tasks=record.num_tasks_contributed,
                                avg_quality_score=record.avg_quality_score,
                                num_audits_edited=record.num_audits_edited,
                                num_audits_further_improved=record.num_audits_reviewed_and_improved,
                            )
                            lb_record.blended_points = round(aya_score_for_language)
                            lb_record.quality_score = round(record.avg_quality_score, 2)
                else:
                    # this can happen because a user may have contributed to a language
                    # but not have any audits or reviews
                    # and therefore not have a quality score or aya score
                    logger.warning(f'no aya score found for user_id: {lb_record.user_id} and username: {lb_record.username}')

                if lb_record.blended_points is None:
                    lb_record.blended_points = 0
                    lb_record.quality_score = 0
                    lb_record.blended_rank = 0

            # then re-rank the users based on the number of blended points they have earned
            # within each of there language groups
            leaderboard_records = update_blended_ranks_within_language_groups(
                leaderboard_records,
            )

            # then commit the changes to the database
            session.commit()
    except Exception as e:
        logger.error(f'error while updating blended ranking and points for language leaderboard: {e}')
        raise e
    else:
        logger.info('blended ranking and points updated for language leaderboard!')

update_leaderboard_by_language()
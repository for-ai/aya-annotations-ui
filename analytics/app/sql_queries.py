TASK_1_TOP_CONTRIBUTORS_QUERY = """
    WITH generated_task_audit_submissions
    AS
    (
    SELECT
        u.username                AS username,
        lc.name                   AS language,
        count(*)       AS num_submissions
    FROM
        task_audit ta
    INNER JOIN "user" u ON ta.submitted_by = u.id
    INNER JOIN task t ON ta.task_id = t.id
    INNER JOIN language_code lc ON t.language_id = lc.id
    GROUP BY
        u.username,
        lc.name
    ORDER BY num_submissions desc
    ),

    contributed_task_audit_submissions
    AS 
    (
    SELECT
        u.username                AS username,
        lc.name                   AS language,
        count(*)       AS num_submissions
    FROM
        task_contribution_audit tca
    INNER JOIN "user" u ON tca.submitted_by = u.id
    INNER JOIN task_contribution ta ON tca.task_contribution_id = ta.id
    INNER JOIN language_code lc ON ta.language_id = lc.id
    GROUP BY
        u.username,
        lc.name
    ORDER BY num_submissions desc
    )

    SELECT 
        username, 
        language, 
        SUM(num_submissions) AS number_of_unique_submissions
    FROM 
    (
    SELECT username, language, num_submissions
    FROM
    (
    SELECT * FROM generated_task_audit_submissions
    UNION ALL
    SELECT * FROM contributed_task_audit_submissions
    ) AS combined_results
    ) AS final_results
    GROUP BY
        username,
        language
    ORDER BY 
        number_of_unique_submissions DESC;
    """

TASK_2_TOP_CONTRIBUTORS_QUERY = """
    SELECT
        u.username AS USERNAME,
        lc.name AS LANGUAGE,
        count(*) AS NUMBER_OF_UNIQUE_SUBMISSIONS
    FROM
        task_contribution tc
    INNER JOIN "user" u ON tc.submitted_by = u.id
    INNER JOIN language_code lc ON tc.language_id = lc.id
    GROUP BY
        lc.name,
        u.username
    ORDER BY NUMBER_OF_UNIQUE_SUBMISSIONS DESC
"""

NUM_AUDITED_GENERATED_TASKS_QUERY = """
    SELECT count(*) FROM task_audit ta
    JOIN task t ON t.id = ta.task_id
    JOIN dataset ds ON t.dataset_id = ds.id
    WHERE ds.active = TRUE
    """

NUM_AUDITED_CONTRIBUTED_TASKS_QUERY = """
    SELECT count(*) FROM task_contribution_audit tca
    JOIN task_contribution tc ON tc.id = tca.task_contribution_id
    """

TASK_2_NUM_SUBMISSIONS_QUERY = """
    SELECT count(*) FROM task_contribution
    """

ALL_SUBMITTED_TASKS_COUNT_QUERY = f"""
    (
    {NUM_AUDITED_CONTRIBUTED_TASKS_QUERY}
    ) AS num_audited_contributed_tasks,
    (
    {NUM_AUDITED_GENERATED_TASKS_QUERY}
    ) AS num_audited_generated_tasks,
    
    (
    {TASK_2_NUM_SUBMISSIONS_QUERY}
    ) AS num_contributed_new_tasks
"""

TOTAL_USER_COUNT_QUERY = """SELECT count(*) FROM public.user"""

TOTAL_USERS_AUDITING_CONTRIBUTED_TASKS_QUERY = (
    """SELECT COUNT(DISTINCT submitted_by) FROM task_contribution_audit"""
)

TOTAL_USERS_AUDITING_GENERATED_TASKS_QUERY = (
    """SELECT COUNT(DISTINCT submitted_by) FROM task_audit"""
)

TOTAL_USERS_CONTRIBUTING_NEW_TASKS_QUERY = (
    """SELECT COUNT(DISTINCT submitted_by) FROM task_contribution"""
)

TASK_1_USERS = """ 
    WITH task_1_users
    AS
   (SELECT DISTINCT submitted_by FROM task_contribution_audit
   UNION
   SELECT DISTINCT submitted_by FROM task_audit
   )

   SELECT count(*) FROM task_1_users
"""

ALL_USERS_COUNT_QUERY = f"""
    (
    {TOTAL_USER_COUNT_QUERY}
    ) AS total_registered_users,
    (
    {TOTAL_USERS_AUDITING_CONTRIBUTED_TASKS_QUERY}
    ) AS num_users_auditing_contributed_tasks,
    (
    {TOTAL_USERS_AUDITING_GENERATED_TASKS_QUERY}
    ) AS num_users_audited_generated_tasks,
    (
    {TASK_1_USERS}
    ) AS task_1_user_count,
    (
    {TOTAL_USERS_CONTRIBUTING_NEW_TASKS_QUERY}
    ) AS num_users_contributing_new_tasks
"""

ALL_USER_TASK_QUERY = f"""SELECT
{ALL_USERS_COUNT_QUERY},
{ALL_SUBMITTED_TASKS_COUNT_QUERY};
"""

USERS_AUDITING_GENERATED_TASKS_QUERY = """
    SELECT 
        username, 
        count(*) as num_submissions,
        lc.name as language
    FROM task_audit
    JOIN public.user ON public.user.id = task_audit.submitted_by
    JOIN task ON task.id = task_audit.task_id
    JOIN language_code lc ON lc.id = task.language_id
    GROUP BY username, lc.name
    ORDER BY num_submissions desc;
"""

USERS_AUDITING_CONTRIBUTED_TASKS_QUERY = """
   SELECT 
        username, 
        count(*) as num_submissions,
        lc.name as language
    FROM task_contribution_audit tca
    JOIN public.user ON public.user.id = tca.submitted_by
    JOIN task_contribution tc ON tc.id = tca.task_contribution_id	
    JOIN language_code lc ON lc.id = tc.language_id
    GROUP BY username, lc.name
    ORDER BY num_submissions desc;
"""

USERS_CONTRIBUTING_NEW_TASKS_QUERY = """
    SELECT 
        username, 
        count(*) as num_submissions,
        lc.name as language
    FROM task_contribution tc
    JOIN public.user ON public.user.id = tc.submitted_by
    JOIN language_code lc ON lc.id = tc.language_id
    GROUP BY username, lc.name
    ORDER BY num_submissions desc;
"""


# This query is referred & modified from - instruct-multilingual-web-app/backend/jobs/by_language/leaderboard_by_language_job.py
TASK_1_GENERATED_AUDITED_TASKS_QUERY = """
    SELECT
        u.id                      AS user_id,
        u.username                AS username,
        lc.name                   AS language,
        lc.code                   AS language_code,
        cc.name                   AS country,
        COALESCE(SUM(1), 0)       AS submission_count
    FROM
        task_audit ta
    INNER JOIN
        "user" u
    ON
        ta.submitted_by = u.id
    INNER JOIN
        task t
    ON
        ta.task_id = t.id
    INNER JOIN
        language_code lc
    ON
        t.language_id = lc.id
    INNER JOIN 
        "country_code" cc 
    ON 
        u.country_code = cc.id
    GROUP BY
        u.id,
        u.username,
        lc.name,
        cc.name,
        lc.code
    """

TASK_1_CONTRIBUTED_AUDITED_TASKS_QUERY = """
    SELECT
        u.id                AS user_id,
        u.username          AS username,
        lc.name             AS language,
        lc.code             AS language_code,
        cc.name             AS country,
        COALESCE(SUM(1), 0) AS submission_count
    FROM
        task_contribution_audit tca
    INNER JOIN 
        "user" u 
    ON 
        tca.submitted_by = u.id
    INNER JOIN 
        task_contribution tc 
    ON 
        tca.task_contribution_id = tc.id
    INNER JOIN 
        language_code lc 
    ON 
        tc.language_id = lc.id
    INNER JOIN 
        "country_code" cc 
    ON 
        u.country_code = cc.id
    GROUP BY
        u.id,
        lc.name,
        u.username,
        cc.name,
        lc.code
"""


TASK_1_LANGUAGE_LEADERBOARD_QUERY = f"""
    WITH generated_task_audited_leaderboard
    AS
    (
    {TASK_1_GENERATED_AUDITED_TASKS_QUERY}
    ),

    contributed_task_audited_leaderboard
    AS 
    (
    {TASK_1_CONTRIBUTED_AUDITED_TASKS_QUERY}
    )
    
    SELECT 
        user_id,
        username,
        language,
        language_code,
        country,
        SUM(submission_count) AS num_submissions
    FROM 
    (
    SELECT 
        user_id,
        username,
        language,
        language_code,
        country,
        submission_count
    FROM
    (
    SELECT * FROM generated_task_audited_leaderboard
    UNION ALL
    SELECT * FROM contributed_task_audited_leaderboard
    ) AS combined_results
    ) AS final_results
    GROUP BY
        user_id,
        username,
        language,
        language_code,
        country
    ORDER BY 
        num_submissions DESC;
    """

# This query is referred from - instruct-multilingual-web-app/backend/jobs/by_language/leaderboard_by_language_job.py
TASK_2_LANGUAGE_LEADERBOARD_QUERY = """
    SELECT
        u.id                        AS user_id,
        u.username                  AS username,
        lc.name                     AS language,
        lc.code                     AS language_code,
        cc.name                     AS country,
        COALESCE(SUM(1), 0)         AS num_submissions,
        u.image_url                 AS image_url
        
    FROM
        task_contribution tc
    INNER JOIN "user" u ON tc.submitted_by = u.id
    INNER JOIN language_code lc ON tc.language_id = lc.id
    INNER JOIN "country_code" cc ON u.country_code = cc.id
    GROUP BY
        u.id,
        lc.name,
        u.username,
        u.image_url,
        lc.code,
        cc.name
    """

GIVEN_DATE = None

DATE_SPECIFIC_TASK_1_LANG_LEADERBOARD = f"""
    SELECT
        user_id,
        username,
        language,
        country,
        SUM(submission_count) AS num_submissions
    FROM (
        SELECT
            user_id,
            username,
            language,
            country,
            submission_count
        FROM (
            SELECT
                u.id                         AS user_id,
                u.username                   AS username,
                lc.name                      AS language,
                cc.name             AS country,
                COALESCE(SUM(1), 0) AS submission_count
            FROM
                task_audit ta
            INNER JOIN "user" u ON ta.submitted_by = u.id
            INNER JOIN task t ON ta.task_id = t.id
            INNER JOIN language_code lc ON t.language_id = lc.id
            INNER JOIN "country_code" cc ON u.country_code = cc.id
            WHERE
                DATE_TRUNC('day', ta.created_at) = '{GIVEN_DATE}'
            GROUP BY
                u.id,
                lc.name,
                u.username,
                cc.name

            UNION ALL

            SELECT
                u.id                AS user_id,
                u.username          AS username,
                lc.name             AS language,
                cc.name             AS country,
                COALESCE(SUM(1), 0) AS submission_count
            FROM
                task_contribution_audit tca
            INNER JOIN "user" u ON tca.submitted_by = u.id
            INNER JOIN task_contribution tc ON tca.task_contribution_id = tc.id
            INNER JOIN language_code lc ON tc.language_id = lc.id
            INNER JOIN "country_code" cc ON u.country_code = cc.id
            WHERE
                DATE_TRUNC('day', tca.created_at) = '{GIVEN_DATE}'
            GROUP BY
                u.id,
                lc.name,
                u.username,
                cc.name

        ) AS combined_results
    ) AS final_results
    GROUP BY
        user_id,
        username,
        language,
        country
    ORDER BY
        num_submissions DESC;
    """
import pandas as pd
from typing import Dict, Optional, List
from collections import Counter
from utils import connect_to_db_with_connector, convert_country_to_continent
from constants import (
    NUM_SUBMISSIONS_COL_NAME,
    LANGUAGE_REGION_DICT,
    TASK_1_NAME,
    AFRICA_REGION,
    ASIA_REGION,
    EUROPE_REGION,
    LATAM_REGION,
    OTHERS_REGION,
    ALL_LANG_COL_NAME,
    ALL_REGION_COL_NAME
)
from sql_queries import (
    TASK_1_LANGUAGE_LEADERBOARD_QUERY,
    TASK_2_LANGUAGE_LEADERBOARD_QUERY,
    TASK_1_TOP_CONTRIBUTORS_QUERY,
    TASK_2_TOP_CONTRIBUTORS_QUERY,
    ALL_USER_TASK_QUERY,
    USERS_AUDITING_CONTRIBUTED_TASKS_QUERY,
    USERS_AUDITING_GENERATED_TASKS_QUERY,
    USERS_CONTRIBUTING_NEW_TASKS_QUERY,
)

connection = connect_to_db_with_connector()


def get_date_filtered_task_leaderboards(submission_date: str, task_name) -> pd.DataFrame:

    DATE_FILTERED_TASK_1_LANG_LEADERBOARD = f"""
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
                DATE_TRUNC('day', ta.created_at) <= '{submission_date}'
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
                DATE_TRUNC('day', tca.created_at) <= '{submission_date}'
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


    DATE_FILTERED_TASK_2_LANG_LEADERBOARD = f"""
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
    WHERE
        DATE_TRUNC('day', tc.created_at) <= '{submission_date}'
    GROUP BY
        u.id,
        lc.name,
        u.username,
        u.image_url,
        lc.code,
        cc.name
    """

    filter_lang_leaderboard_query = (
            DATE_FILTERED_TASK_1_LANG_LEADERBOARD
            if task_name == TASK_1_NAME
            else DATE_FILTERED_TASK_2_LANG_LEADERBOARD
        )

    return filter_lang_leaderboard_query

def calculate_growth_percentage(submissions_start_date, submissions_end_date):
    if submissions_start_date == 0 and submissions_end_date == 0:
        growth_percent = 0
    elif submissions_start_date == 0 and submissions_end_date != 0:
        growth_percent = float('inf')
    else:
        growth_percent = round((((submissions_end_date - submissions_start_date) / submissions_start_date) * 100), 2)

    return growth_percent


def calculate_lang_growth(start_date: str, end_date: str, task_name: str, region_filter: str, lang_filter: str):

    start_date_leaderboard_query = get_date_filtered_task_leaderboards(start_date, task_name)

    start_date_leaderboard = calculate_region_specific_scores(task_name, region_filter, lang_filter, leaderboard_query=start_date_leaderboard_query)
    start_date_leaderboard = start_date_leaderboard.drop(['REGION'], axis =1)
    start_date_leaderboard = start_date_leaderboard.rename(columns={NUM_SUBMISSIONS_COL_NAME: "NUM_SUBMISSIONS_START_DATE"})

    end_date_leaderboard_query = get_date_filtered_task_leaderboards(end_date, task_name)

    end_date_leaderboard = calculate_region_specific_scores(task_name, region_filter, lang_filter, leaderboard_query=end_date_leaderboard_query)
    end_date_leaderboard = end_date_leaderboard.drop(['REGION'], axis =1)
    end_date_leaderboard = end_date_leaderboard.rename(columns={NUM_SUBMISSIONS_COL_NAME: "NUM_SUBMISSIONS_END_DATE"})

    growth_leaderboard = pd.merge(start_date_leaderboard, end_date_leaderboard, how="outer", on=["LANGUAGE"])

    growth_leaderboard = growth_leaderboard.fillna(0)

    growth_leaderboard['NUM_SUBMSSIONS_ADDED'] =  growth_leaderboard.apply(lambda x: (x["NUM_SUBMISSIONS_END_DATE"] - x["NUM_SUBMISSIONS_START_DATE"]), axis=1)

    growth_leaderboard['GROWTH_PERCENTAGE'] = growth_leaderboard.apply(lambda x: calculate_growth_percentage(x["NUM_SUBMISSIONS_START_DATE"], x["NUM_SUBMISSIONS_END_DATE"]), axis=1)

    growth_leaderboard = growth_leaderboard.sort_values(
        by=['GROWTH_PERCENTAGE'], ascending=False
    )

    return growth_leaderboard



def get_task_specific_language_leaderboard(lang_leaderboard_query: str) -> pd.DataFrame:
    """Get the language leaderboard for a given task (e.g. Rate Model Performance)

    Args:
        lang_leaderboard_query (str): The query to be used to calculate the overall language leaderboard for a task.

    Returns:
        pd.DataFrame: Dataframe containing overall language leaderboard for a task.
    """
    lang_leaderboard = pd.read_sql(lang_leaderboard_query, connection)

    # create 'continent' column based on 'country' of contributors
    lang_leaderboard["continent"] = lang_leaderboard["country"].apply(
        lambda country_name: convert_country_to_continent(country_name)
    )
    return lang_leaderboard


def get_task_specific_language_scores(task_name: str, leaderboard_query: str = None) -> Dict:
    """Helper function to calculate the total submissions made for all languages for a particular task.

    Args:
        task_name (str): Name of the task (e.g 'Rate Model Performance' or 'Contribute your Languge')

    Returns:
        Dict: A dict mapping languages to the number of submissions received for them.
    """
    if leaderboard_query is None: 
        language_leaderboard_query = (
            TASK_1_LANGUAGE_LEADERBOARD_QUERY
            if task_name == TASK_1_NAME
            else TASK_2_LANGUAGE_LEADERBOARD_QUERY
        )
    else:
        language_leaderboard_query = leaderboard_query

    # call helper function to calculate overall language leaderboard for a given task
    language_leaderboard = get_task_specific_language_leaderboard(
        language_leaderboard_query
    )

    unique_languages = list(dict(Counter(language_leaderboard["language"])).keys())
    language_score_map = {}

    for lang in unique_languages:
        current_lang_df = language_leaderboard[language_leaderboard["language"] == lang]

        # split submissions for 'Spanish' & 'Portuguese' based on region of contributors (Europe & LatAm)
        if lang == "Spanish" or lang == "Portuguese":
            europe_col_name = lang + " (Europe)"
            latam_col_name = lang + " (LatAm)"
            language_score_map[europe_col_name] = current_lang_df[
                current_lang_df["continent"] == "Europe"
            ]["num_submissions"].sum()
            language_score_map[latam_col_name] = current_lang_df[
                current_lang_df["continent"] != "Europe"
            ]["num_submissions"].sum()

        # similarly split submissions for standard arabic based on region of contributors (Asia & Africa)
        elif lang == "Standard Arabic":
            asia_col_name = lang + " (Asia)"
            africa_col_name = lang + " (Africa)"
            africa_arabic_df = current_lang_df[current_lang_df["continent"] == "Africa"]
            asian_arabic_df = current_lang_df[current_lang_df["continent"] != "Africa"]
            language_score_map[africa_col_name] = africa_arabic_df[
                "num_submissions"
            ].sum()
            language_score_map[asia_col_name] = asian_arabic_df["num_submissions"].sum()

        else:
            language_score_map[lang] = current_lang_df["num_submissions"].sum()

    return language_score_map


def calculate_region_specific_scores(
    task_name: str, region_name: str = "ALL REGIONS", language_name: str = "All Languages", leaderboard_query: str = None,
) -> pd.DataFrame:
    """Calculate the total submissions made for all languages of a given region for a particular task.

    Args:
        task_name (str): Name of the task (e.g 'Rate Model Performance' or 'Contribute your Languge')
        region_name (str): Name of the region (continent) for we need to calculate submissions
    Returns:
        pd.DataFrame: DataFrame containing languages with and their total submissions.
    """
    language_score_map = {}

    # calculate total numbers of submissions for all languages for which contributions were received.
    language_score_map = get_task_specific_language_scores(task_name, leaderboard_query)

    def map_language_to_region(language):
        region_name = "ADDITIONAL"
        for region, _ in LANGUAGE_REGION_DICT.items():
            region_specific_languages = LANGUAGE_REGION_DICT[region]
            
            if language in region_specific_languages:
                region_name = region
                break
        return region_name
    
    # update `language_score_map` with names of languages that have no contributions
    lang_with_no_contributions = [lang for region,_ in LANGUAGE_REGION_DICT.items() for lang in LANGUAGE_REGION_DICT[region] if lang not in language_score_map.keys()]

    for language in lang_with_no_contributions:
        language_score_map[language] = 0

    region_lang_scores = {
        "LANGUAGE": language_score_map.keys(),
        NUM_SUBMISSIONS_COL_NAME: language_score_map.values(),
    }
    region_lang_df = pd.DataFrame(region_lang_scores).sort_values(
        by=[NUM_SUBMISSIONS_COL_NAME], ascending=False
    )
    
    # add a 'REGION' column to the dataframe specifying which region does a language fall under for Aya
    region_lang_df["REGION"] = region_lang_df["LANGUAGE"].apply(
        lambda language_name: map_language_to_region(language_name)
    )
    
    # filter out submissions for languages related to a particular region based on `region_name`
    if region_name == "ALL REGIONS":
        region_lang_df = region_lang_df[region_lang_df["REGION"] != "ADDITIONAL"]
    else:
        region_lang_df = region_lang_df[region_lang_df["REGION"] == region_name]
    
    # filter out submissions for a particular language if specified
    if language_name != "All Languages":
        region_lang_df = region_lang_df[
            region_lang_df["LANGUAGE"].str.contains(language_name)
        ]

    return region_lang_df


def calculate_all_region_scores(task_name: str) -> pd.DataFrame:
    """Calculate total region specific submissions for a given task.

    Args:
        task_name (str): Name of the task (e.g 'Rate Model Performance' or 'Contribute your Languge')
    Returns:
        pd.DataFrame: Dataframe containing total submissions made by a region for a task.
    """

    region_score_map = {
        EUROPE_REGION: 0,
        ASIA_REGION: 0,
        AFRICA_REGION: 0,
        LATAM_REGION: 0,
        OTHERS_REGION: 0,
    }

    language_score_map = get_task_specific_language_scores(task_name)

    for language, score in language_score_map.items():
        for region in LANGUAGE_REGION_DICT.keys():
            regional_languages = LANGUAGE_REGION_DICT[region]
            if language in regional_languages:
                region_score_map[region] += score
                break

    # create DataFrame which will be used for plotting results
    final_scores = {
        ALL_REGION_COL_NAME: region_score_map.keys(),
        NUM_SUBMISSIONS_COL_NAME: region_score_map.values(),
    }
    regional_df = pd.DataFrame(final_scores).sort_values(
        by=[NUM_SUBMISSIONS_COL_NAME], ascending=False
    )
    return regional_df


def get_highest_performing_lang_scores(task_name: str) -> pd.DataFrame:
    """Find the total submissions made for the highest performing top 10 languages for a given task.

    Args:
        task_name (str): Name of the task (e.g 'Rate Model Performance' or 'Contribute your Languge')
    Returns:
        pd.DataFrame: Dataframe containing total submissions made for top 10 languages for a task.
    """
    language_scores = get_task_specific_language_scores(task_name)
    final_lang_scores = {
        ALL_LANG_COL_NAME: language_scores.keys(),
        NUM_SUBMISSIONS_COL_NAME: language_scores.values(),
    }
    overall_lang_df = (
        pd.DataFrame(final_lang_scores)
        .sort_values(by=[NUM_SUBMISSIONS_COL_NAME], ascending=False)
        .head(10)
    )
    return overall_lang_df


def get_languages_with_most_contributors(task_name: str) -> pd.DataFrame:
    """Find the top 10 languages for a given task based on number of contributors.

    Args:
        task_name (str): Name of the task (e.g 'Rate Model Performance' or 'Contribute your Languge')
    Returns:
        pd.DataFrame: Dataframe containing names of top 10 languages based on no. of contributors
    """
    query = (
        TASK_1_TOP_CONTRIBUTORS_QUERY
        if task_name == TASK_1_NAME
        else TASK_2_TOP_CONTRIBUTORS_QUERY
    )
    lang_contributor_df = pd.read_sql(query, connection)
    lang_with_most_contributors = dict(
        Counter(lang_contributor_df["language"]).most_common(10)
    )

    # create DataFrame which will be used for plotting results
    lang_contributors = {
        ALL_LANG_COL_NAME: lang_with_most_contributors.keys(),
        "NUMBER_OF_CONTRIBUTORS": lang_with_most_contributors.values(),
    }
    overall_lang_contributor_df = pd.DataFrame(lang_contributors).sort_values(
        by=["NUMBER_OF_CONTRIBUTORS"], ascending=False
    )
    return overall_lang_contributor_df


def get_top_contributors(task_name: str) -> pd.DataFrame:
    """Find the overall top 10 contributors for a given task.

    Args:
        task_name (str): Name of the task (e.g 'Rate Model Performance' or 'Contribute your Languge')

    Returns:
        pd.DataFrame: Dataframe containing submission details of top 10 users based on no. of submissions for a task.
    """
    contributor_query = (
        TASK_1_TOP_CONTRIBUTORS_QUERY
        if task_name == TASK_1_NAME
        else TASK_2_TOP_CONTRIBUTORS_QUERY
    )

    top_contributor_scores = pd.read_sql(contributor_query, connection)

    return top_contributor_scores.sort_values(
        by=["number_of_unique_submissions"], ascending=False
    ).head(10)


def get_task_and_user_general_stats() -> int:
    """Get general stats about tasks & users including:
        1. Total number of submissions made for all tasks along
        2. Number of users who made submissions for all tasks

    Returns:
        pd.DataFrame:
    """

    general_stats = pd.read_sql(ALL_USER_TASK_QUERY, connection)

    return general_stats


def get_user_submissions():
    generated_audit_submissions = pd.read_sql(
        USERS_AUDITING_GENERATED_TASKS_QUERY, connection
    )

    contributed_audit_submissions = pd.read_sql(
        USERS_AUDITING_CONTRIBUTED_TASKS_QUERY, connection
    )

    contributing_new_submissions = pd.read_sql(
        USERS_CONTRIBUTING_NEW_TASKS_QUERY, connection
    )

    return (
        generated_audit_submissions,
        contributed_audit_submissions,
        contributing_new_submissions,
    )

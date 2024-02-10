import os
import gradio as gr
from constants import (
    NUM_SUBMISSIONS_COL_NAME,
    TASK_1_NAME,
    TASK_2_NAME,
    ALL_LANG_COL_NAME,
    TOP_LANG_PLOT,
    TOP_CONTRIBUTOR_PLOT,
    TOP_LANG_CONTRIBUTOR_PLOT,
    ASIA_REGION,
    EUROPE_REGION,
    AFRICA_REGION,
    LATAM_REGION,
    OTHERS_REGION,
    ENV_FILE_PATH,
    DB_LANGUAGE_LIST,
    MT5_LANGUAGE_LIST,
)
from analytics import (
    calculate_lang_growth,
    calculate_growth_percentage,
    calculate_all_region_scores,
    calculate_region_specific_scores,
    get_highest_performing_lang_scores,
    get_top_contributors,
    get_languages_with_most_contributors,
    get_task_and_user_general_stats,
    get_user_submissions,
)
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(ENV_FILE_PATH)

gradio_server_name = os.environ["GRADIO_SERVER_NAME"]
gradio_server_port = os.environ["GRADIO_SERVER_PORT"]

today_date = datetime.today()


def create_bar_plot(plot_data, xlabel, ylabel, plot_title):
    return gr.BarPlot.update(
        plot_data,
        x=xlabel,
        y=ylabel,
        title=plot_title,
        tooltip=[xlabel, ylabel],
        height=300,
        width=300,
        vertical=False,
    )


def get_all_region_data():
    task_1_data = calculate_all_region_scores(TASK_1_NAME)
    task_2_data = calculate_all_region_scores(TASK_2_NAME)
    return task_1_data, task_2_data


def create_barplot_for_regional_data():
    xlabel = "REGION"
    task_1_plot_title = "Task 1 - Regional Leaderboard"
    task_2_plot_title = "Task 2 - Regional Leaderboard"

    # fetch data to create barplots
    task_1_data, task_2_data = get_all_region_data()

    # create title for plots
    if task_1_plot_title is None and task_2_plot_title is None:
        task_1_plot_title = f"Task 1: {xlabel.lower()} - Contribution Breakdown"
        task_2_plot_title = f"Task 2: {xlabel.lower()}- Contribution Breakdown"

    ylabel = NUM_SUBMISSIONS_COL_NAME

    # create Task 1 plot
    task_1_region_plot = create_bar_plot(task_1_data, xlabel, ylabel, task_1_plot_title)
    # Create Task 2 Plot
    task_2_region_plot = create_bar_plot(task_2_data, xlabel, ylabel, task_2_plot_title)
    return task_1_region_plot, task_2_region_plot


def get_region_based_task_analytics(region_filter, language_filter):
    task1_sum_reset, task2_sum_reset = 0, 0
    task_1_data = calculate_region_specific_scores(
        TASK_1_NAME, region_filter, language_filter
    )
    task_2_data = calculate_region_specific_scores(
        TASK_2_NAME, region_filter, language_filter
    )
    return task_1_data, task_2_data, task1_sum_reset, task2_sum_reset


def plot_highest_performing_languages(task_lang_df, task_name):
    xlabel = ALL_LANG_COL_NAME
    ylabel = NUM_SUBMISSIONS_COL_NAME
    task_type = "Task 1" if task_name == TASK_1_NAME else "Task 2"
    plot_title = "Overall Top 10 Languages Scoreboard for " + task_type
    overall_top_lang_plot = create_bar_plot(task_lang_df, xlabel, ylabel, plot_title)
    return overall_top_lang_plot


def plot_highest_performing_contributors(task_lang_df, task_name):
    xlabel = "username"
    ylabel = "number_of_unique_submissions"
    task_type = "Task 1" if task_name == TASK_1_NAME else "Task 2"
    plot_title = "Overall Top 10 Contributors Scoreboard for " + task_type
    overall_top_lang_plot = create_bar_plot(task_lang_df, xlabel, ylabel, plot_title)
    return overall_top_lang_plot


def plot_languages_with_most_contributors(task_lang_df, task_name):
    xlabel = "LANGUAGE"
    ylabel = "NUMBER_OF_CONTRIBUTORS"
    task_type = "Task 1" if task_name == TASK_1_NAME else "Task 2"
    plot_title = "Languages with most no.of contributors for " + task_type
    overall_top_lang_plot = create_bar_plot(task_lang_df, xlabel, ylabel, plot_title)
    return overall_top_lang_plot


def create_overall_performance_plots(plot_type: str):
    task_1_df, task_2_df = get_overall_task_analytics(plot_type)
    if plot_type == TOP_LANG_PLOT:
        task_1_top_lang_plot = plot_highest_performing_languages(task_1_df, TASK_1_NAME)
        task_2_top_lang_plot = plot_highest_performing_languages(task_2_df, TASK_2_NAME)
        return task_1_top_lang_plot, task_2_top_lang_plot

    elif plot_type == TOP_CONTRIBUTOR_PLOT:
        task_1_top_contributor_plot = plot_highest_performing_contributors(
            task_1_df, TASK_1_NAME
        )
        task_2_top_contributor_plot = plot_highest_performing_contributors(
            task_2_df, TASK_2_NAME
        )
        return task_1_top_contributor_plot, task_2_top_contributor_plot

    elif plot_type == TOP_LANG_CONTRIBUTOR_PLOT:
        task_1_lang_contributor_plot = plot_languages_with_most_contributors(
            task_1_df, TASK_1_NAME
        )
        task_2_lang_contributor_plot = plot_languages_with_most_contributors(
            task_2_df, TASK_2_NAME
        )
        return task_1_lang_contributor_plot, task_2_lang_contributor_plot


def get_overall_task_analytics(plot_type):
    if plot_type == TOP_LANG_PLOT:
        task_1_top_lang_df = get_highest_performing_lang_scores(TASK_1_NAME)
        task_2_top_lang_df = get_highest_performing_lang_scores(TASK_2_NAME)
        return task_1_top_lang_df, task_2_top_lang_df

    elif plot_type == TOP_CONTRIBUTOR_PLOT:
        task_1_top_contributor_df = get_top_contributors(TASK_1_NAME)
        task_2_top_contributor_df = get_top_contributors(TASK_2_NAME)
        return task_1_top_contributor_df, task_2_top_contributor_df

    elif plot_type == TOP_LANG_CONTRIBUTOR_PLOT:
        task_1_lang_contributor_df = get_languages_with_most_contributors(TASK_1_NAME)
        task_2_lang_contributor_df = get_languages_with_most_contributors(TASK_2_NAME)
        return task_1_lang_contributor_df, task_2_lang_contributor_df


def compute_general_stats():
    general_stats = get_task_and_user_general_stats()

    # total number of users who have registered using Aya annotation tool
    num_all_users = general_stats["total_registered_users"].iloc[0]

    # number of users who have been auditing generated tasks under 'Task 1'
    num_users_auditing_generated_tasks = general_stats[
        "num_users_audited_generated_tasks"
    ].iloc[0]
    # number of users who have been auditing contributed tasks under 'Task 1'
    num_users_auditing_contributed_tasks = general_stats[
        "num_users_auditing_contributed_tasks"
    ].iloc[0]
    # total number of users contributing for task 1
    num_task_1_users = general_stats["task_1_user_count"].iloc[0]
    # number of users who have been adding new contributions via 'Task 2'
    num_task_2_users = general_stats["num_users_contributing_new_tasks"].iloc[0]

    # How many tasks have been submitted of the type ('generated_audit')
    num_audited_generated_tasks = general_stats["num_audited_generated_tasks"].iloc[0]
    # How many tasks have been submitted of the type ('contributed_audit')
    num_audited_contributed_tasks = general_stats["num_audited_contributed_tasks"].iloc[
        0
    ]
    # Total submissions made for task 1
    num_task_1_tasks = num_audited_contributed_tasks + num_audited_generated_tasks
    # How many tasks have been submitted overall for Task 2
    num_task_2_tasks = general_stats["num_contributed_new_tasks"].iloc[0]

    return (
        num_all_users,
        num_task_1_users,
        num_users_auditing_contributed_tasks,
        num_users_auditing_generated_tasks,
        num_task_2_users,
        num_task_1_tasks,
        num_audited_generated_tasks,
        num_audited_contributed_tasks,
        num_task_2_tasks,
    )


def filter_user_submissions(language_name):
    (
        audited_generated_task_df,
        audited_contributed_task_df,
        contributed_new_task_df,
    ) = get_user_submissions()

    filtered_audited_generated_task_df = audited_generated_task_df[
        audited_generated_task_df["language"] == language_name
    ]
    filtered_audited_contributed_task_df = audited_contributed_task_df[
        audited_contributed_task_df["language"] == language_name
    ]
    filtered_contributed_new_task_df = contributed_new_task_df[
        contributed_new_task_df["language"] == language_name
    ]

    return (
        filtered_audited_generated_task_df,
        filtered_audited_contributed_task_df,
        filtered_contributed_new_task_df,
    )


def compute_task_submissions(task_df):
    num_submissions = task_df["NUMBER OF UNIQUE SUBMISSIONS"].sum()
    return num_submissions


def compute_total_growth(task_growth_df):
    num_submissions_start_date = task_growth_df["NUM_SUBMISSIONS_START_DATE"].sum()
    num_submissions_end_date = task_growth_df["NUM_SUBMISSIONS_END_DATE"].sum()
    total_growth = calculate_growth_percentage(num_submissions_start_date, num_submissions_end_date)
    return num_submissions_start_date, num_submissions_end_date, total_growth

def calculate_growth(start_date_day, start_date_month, start_date_year, end_date_day, end_date_month, end_date_year,
                     task_choice, region_choice, lang_choice):

    start_date = f"{start_date_year}-{start_date_month}-{start_date_day}"
    end_date = f"{end_date_year}-{end_date_month}-{end_date_day}"

    task_growth_df = calculate_lang_growth(start_date, end_date, task_choice, region_choice, lang_choice)

    return task_growth_df


with gr.Blocks(theme="shivi/calm_seafoam") as demo:
    with gr.Row(variant="panel"):
        with gr.Column():
            gr.HTML(
                """<html><img src='file/logo/aya_logo.png', alt='Aya logo', width=150, height=150 /><br></html>"""
            )
        with gr.Column():
            gr.HTML(
                """<p style="text-align: center; font-weight: bold; font-size: 15px;">Aya: An Open Science Initiative to Accelerate Multilingual AI Progress</p>"""
            )
            gr.Markdown(
                "Aya is an open science project that aims to build a multilingual language model via instruction tuning that harnesses the collective wisdom and contributions of people from all over the world. With Aya, we want to improve available multilingual generative models and accelerate progress for languages across the world. Contributing to Aya is open to anyone who is passionate about advancing the field of NLP and is committed to promoting open science. By joining Aya, you become part of a global movement dedicated to democratizing access to language technology."
            )

    with gr.TabItem("Regional Analytics"):
        with gr.TabItem("Graphical View") as regional_analytics_graph_view:
            with gr.Row():
                with gr.Column():
                    plot = gr.BarPlot(show_label=False).style(container=True)
                with gr.Column():
                    plot2 = gr.BarPlot(show_label=False).style(container=True)

        with gr.TabItem("Tabular View") as regional_analytics_tabular_view:
            with gr.Row():
                with gr.Column(variant="Panel"):
                    all_region_task1_df = gr.Dataframe(
                        datatype=["str", "number"], label="TASK 1 BREAKDOWN"
                    )
                with gr.Column(variant="Panel"):
                    all_region_task2_df = gr.Dataframe(
                        datatype=["str", "number"], label="TASK 2 BREAKDOWN"
                    )

    with gr.TabItem("Language Analytics") as language_analytics:
        with gr.TabItem("Overall Task Submissions") as language_tabular_view:
            with gr.Row():
                with gr.Column():
                    language_choice = gr.Dropdown(
                        choices=MT5_LANGUAGE_LIST,
                        value="All Languages",
                        label="Filter by Language",
                    )

                with gr.Column(variant="Panel"):
                    region_filter = gr.Dropdown(
                        choices=[
                            "ALL REGIONS",
                            ASIA_REGION,
                            EUROPE_REGION,
                            AFRICA_REGION,
                            LATAM_REGION,
                            OTHERS_REGION,
                            "ADDITIONAL"
                        ],
                        value="ALL REGIONS",
                        label="Filter by Region",
                    )
            with gr.Row():
                with gr.Column(variant="Panel"):
                    task1_df = gr.Dataframe(
                        datatype=["str", "number"],
                        label="TASK 1 BREAKDOWN",
                        interactive=False,
                    )
                with gr.Column(variant="Panel"):
                    task2_df = gr.Dataframe(
                        datatype=["str", "number"],
                        label="TASK 2 BREAKDOWN",
                        interactive=False,
                    )
            with gr.Row():
                with gr.Column():
                    task1_sum = gr.Number(label="Total no. of submissions for Task 1")
                    task1_sum_btn = gr.Button(value="Compute Total Submissions")

                with gr.Column():
                    task2_sum = gr.Number(label="Total no. of submissions for Task 2")
                    task2_sum_btn = gr.Button(value="Compute Total Submissions")

        with gr.TabItem("Contributor Submissions") as user_submissions:
            with gr.Row():
                language_filter = gr.Dropdown(
                    choices=DB_LANGUAGE_LIST,
                    value="English",
                    label="Choose Language Filter",
                )
            with gr.Row():
                with gr.Column(variant="panel"):
                    gr.Textbox(value="Task 1: Contributor Submissions", show_label=False)
                    with gr.Column(variant="compact"):
                        audited_generated_task_df = gr.Dataframe(
                            datatype=["str", "number"],
                            label="No. of submissions made by users who audited generated tasks",
                        )
                    with gr.Column(variant="compact"):
                        audited_contributed_task_df = gr.Dataframe(
                            datatype=["str", "number"],
                            label="No. of submissions made by users who audited contributed tasks",
                        )

                with gr.Column(variant="compact"):
                    gr.Textbox(value="Task 2: Contributor Submissions", show_label=False)
                    contributed_new_task_df = gr.Dataframe(
                        datatype=["str", "number"],
                        label="No. of submissions made by users who contributed new tasks",
                    )


    with gr.TabItem("Growth Analytics") as growth_analytics:
        with gr.Row():
            with gr.Column():
                gr.Textbox(placeholder="Enter the dates between which you want to calculate growth in submissions", interactive=False, show_label=False)
                
                with gr.Row():
                    with gr.Column():
                        gr.Textbox(placeholder="Start Date", interactive=False, show_label=False)
                    with gr.Row():
                        start_date_day = gr.Dropdown(choices=[day for day in range(1, 32)], label="Day", value='28')
                        start_date_month = gr.Dropdown(choices=[month for month in range(1, 13)], label="Month", value='11')
                        start_date_year = gr.Textbox(label="Year", value=2023)

                with gr.Row():
                    with gr.Column():
                        gr.Textbox(placeholder="End Date", interactive=False, show_label=False)
                    with gr.Row():
                        end_date_day = gr.Dropdown(choices=[day for day in range(1, 32)], label="Day", value=str(today_date.day))
                        end_date_month = gr.Dropdown(choices=[month for month in range(1, 13)], label="Month", value=str(today_date.month))
                        end_date_year = gr.Textbox(label="Year", value=str(today_date.year))


        with gr.Row():

            with gr.Column():
                task_choice = gr.Dropdown(
                    choices=[TASK_1_NAME, TASK_2_NAME],
                    value=TASK_1_NAME,
                    label="Choose Task",
                )

            with gr.Column():
                lang_choice = gr.Dropdown(
                    choices=MT5_LANGUAGE_LIST,
                    value="All Languages",
                    label="Filter by Language",
                )

            with gr.Column(variant="Panel"):
                region_filter_2 = gr.Dropdown(
                    choices=[
                        "ALL REGIONS",
                        ASIA_REGION,
                        EUROPE_REGION,
                        AFRICA_REGION,
                        LATAM_REGION,
                        OTHERS_REGION,
                        "ADDITIONAL"
                    ],
                    value="ALL REGIONS",
                    label="Filter by Region",
                )
            with gr.Column(variant="panel"):
                compute_lang_growth = gr.Button(show_label=False, value="Calculate Growth")

        with gr.Row():
            with gr.Column(variant="Panel"):
                task_growth_df = gr.Dataframe(
                    datatype=["str", "number"],
                    label="GROWTH ACROSS LANGUAGES",
                    interactive=False,
                )

        with gr.Row():
                with gr.Column():
                    start_date_sum = gr.Number(label="Total no. of submissions on Start Date")
                with gr.Column():
                    end_date_sum = gr.Number(label="Total no. of submissions on End Date")
                with gr.Column():
                    total_growth_percent = gr.Number(label="Total Growth Percentage")
                with gr.Column():
                    total_growth_btn = gr.Button(value="Calculate Total Growth")
        

    with gr.TabItem("Overall Analytics") as overall_analytics:
        with gr.TabItem("Graphical View"):
            with gr.Column():
                with gr.Column():
                    lang_plot_type = gr.Dropdown(
                        choices=[
                            TOP_LANG_PLOT,
                            TOP_CONTRIBUTOR_PLOT,
                            TOP_LANG_CONTRIBUTOR_PLOT,
                        ],
                        value=TOP_LANG_PLOT,
                        label="Choose Type of Leaderboard",
                    )
                with gr.Row():
                    with gr.Column():
                        overall_analytics_task1_plot = gr.BarPlot(
                            show_label=False
                        ).style(container=True)
                    with gr.Column():
                        overall_analytics_task2_plot = gr.BarPlot(
                            show_label=False
                        ).style(container=True)

        with gr.TabItem("Tabular View") as overall_analytics_tab_view:
            with gr.Column():
                with gr.Column():
                    leaderboard_type = gr.Dropdown(
                        choices=[
                            TOP_LANG_PLOT,
                            TOP_CONTRIBUTOR_PLOT,
                            TOP_LANG_CONTRIBUTOR_PLOT,
                        ],
                        value=TOP_LANG_PLOT,
                        label="Choose Type of Leaderboard",
                    )
                with gr.Row():
                    with gr.Column(variant="Panel"):
                        overall_analytics_task1_df = gr.Dataframe(
                            datatype=["str", "number"], label="TASK 1 BREAKDOWN"
                        )
                    with gr.Column(variant="Panel"):
                        overall_analytics_task2_df = gr.Dataframe(
                            datatype=["str", "number"], label="TASK 2 BREAKDOWN"
                        )

    with gr.TabItem("General Stats") as general_stats:
        with gr.TabItem("User & Task Stats") as user_task_view:
            with gr.Row():
                total_users = gr.Number(label="Total no. of registered users")

            with gr.Row(variant="panel"):
                with gr.Column():
                    task_1_users = gr.Number(
                        label="Total no. of users contributing for Task 1"
                    )
                with gr.Column():
                    task_1_generated_users = gr.Number(
                        label="Total no. of users who audited generated tasks for Task 1"
                    )
                    task_1_contributed_users = gr.Number(
                        label="Total no. of users who audited contributed tasks for Task 1"
                    )
            with gr.Row():
                task_2_users = gr.Number(
                    label="Total no. of users contributing for Task 2"
                )

            with gr.Row(variant="panel"):
                with gr.Column():
                    audited_tasks = gr.Number(
                        label="Total no. of submissions for Task 1"
                    )
                with gr.Column():
                    total_audited_gen = gr.Number(
                        label="Total no. of audited generated tasks for Task 1"
                    )
                    total_audited_con = gr.Number(
                        label="Total no. of audited contributed tasks for Task 1"
                    )
            with gr.Row():
                contributed_tasks = gr.Number(
                    label="Total no. of submissions for Task 2"
                )

    # On app load
    demo.load(fn=create_barplot_for_regional_data, outputs=[plot, plot2])

    # Regional Analytics
    regional_analytics_graph_view.select(
        create_barplot_for_regional_data, outputs=[plot, plot2]
    )
    regional_analytics_tabular_view.select(
        get_all_region_data, outputs=[all_region_task1_df, all_region_task2_df]
    )

    # Language Analytics
    language_analytics.select(
        get_region_based_task_analytics,
        inputs=[region_filter, language_choice],
        outputs=[task1_df, task2_df, task1_sum, task2_sum],
    )

    # Task submissions view
    language_tabular_view.select(
        get_region_based_task_analytics,
        inputs=[region_filter, language_choice],
        outputs=[task1_df, task2_df, task1_sum, task2_sum],
    )
    language_choice.change(
        get_region_based_task_analytics,
        inputs=[region_filter, language_choice],
        outputs=[task1_df, task2_df, task1_sum, task2_sum],
    )
    region_filter.change(
        get_region_based_task_analytics,
        inputs=[region_filter, language_choice],
        outputs=[task1_df, task2_df, task1_sum, task2_sum],
    )
    task1_sum_btn.click(
        compute_task_submissions, inputs=[task1_df], outputs=[task1_sum]
    )
    task2_sum_btn.click(
        compute_task_submissions, inputs=[task2_df], outputs=[task2_sum]
    )

    # User submissions view
    language_filter.change(
        filter_user_submissions,
        inputs=[language_filter],
        outputs=[
            audited_generated_task_df,
            audited_contributed_task_df,
            contributed_new_task_df,
        ],
    )
    user_submissions.select(
        filter_user_submissions,
        inputs=[language_filter],
        outputs=[
            audited_generated_task_df,
            audited_contributed_task_df,
            contributed_new_task_df,
        ],
    )

    #Growth Analytics

    compute_lang_growth.click(
        calculate_growth, inputs=[start_date_day, start_date_month, start_date_year, end_date_day, end_date_month, end_date_year,
                                  task_choice, region_filter_2, lang_choice], outputs=[task_growth_df]
    )

    total_growth_btn.click(
        compute_total_growth, inputs=[task_growth_df], outputs=[start_date_sum, end_date_sum, total_growth_percent]
    )

    # Overall Analytics
    overall_analytics.select(
        create_overall_performance_plots,
        inputs=lang_plot_type,
        outputs=[overall_analytics_task1_plot, overall_analytics_task2_plot],
    )
    # Overall Analytics - Graphical View
    lang_plot_type.change(
        create_overall_performance_plots,
        inputs=lang_plot_type,
        outputs=[overall_analytics_task1_plot, overall_analytics_task2_plot],
    )

    # Overall Analytics - Tabular View
    overall_analytics_tab_view.select(
        get_overall_task_analytics,
        inputs=leaderboard_type,
        outputs=[overall_analytics_task1_df, overall_analytics_task2_df],
    )
    leaderboard_type.change(
        get_overall_task_analytics,
        inputs=leaderboard_type,
        outputs=[overall_analytics_task1_df, overall_analytics_task2_df],
    )

    # General Stats
    user_task_view.select(
        compute_general_stats,
        outputs=[
            total_users,
            task_1_users,
            task_1_contributed_users,
            task_1_generated_users,
            task_2_users,
            audited_tasks,
            total_audited_gen,
            total_audited_con,
            contributed_tasks,
        ],
    )
    general_stats.select(
        compute_general_stats,
        outputs=[
            total_users,
            task_1_users,
            task_1_contributed_users,
            task_1_generated_users,
            task_2_users,
            audited_tasks,
            total_audited_gen,
            total_audited_con,
            contributed_tasks,
        ],
    )


if __name__ == "__main__":
    demo.launch(
        server_name=gradio_server_name, server_port=int(gradio_server_port), ssl_verify=False
    )

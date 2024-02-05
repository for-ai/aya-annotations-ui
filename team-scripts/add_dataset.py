"""
This script adds a new dataset to the database. The script takes as input a directory of files,
each of which represents a dataset and contains a list of prompts-completions pairs.

The script will create a new dataset in the database, and add randomly sampled prompt-completion pairs
as new tasks and associate the task with the dataset.
"""
import csv
import datetime
import getpass
import io
import json
import os
import logging
import random
import time

from typing import Dict, List, Optional

from pathlib import Path
from pprint import pformat

import sqlalchemy as sa
import requests

from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import insert

import click

load_dotenv(".env.team-instruct-multilingual-app.prod")

logger = logging.getLogger("add-dataset-script")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# Get database URI from environment variable
db_uri = os.environ.get("TEAM_INSTRUCT_MULTILINGUAL_APP_DB_URI_PROD")

if db_uri is None:
    raise Exception(
        "TEAM_INSTRUCT_MULTILINGUAL_APP_DB_URI_PROD environment variable not set"
    )

# bail out if the webhook URL is not set
discord_webhook_url = os.environ.get("DISCORD_ALERTS_WEBHOOK_URL")
if not discord_webhook_url or discord_webhook_url is None:
    logger.warning(
        f"discord webhook URL not set, skipping webhook payload delivery"
    )
    raise Exception(
        "DISCORD_ALERTS_WEBHOOK_URL is not set. Please set it in the .env file. "
        "You can find the value in GCP Secret Manager"
    )


def get_gcp_language_filenames(
    directory: str,
    splits: List[str],
    file_type: str,
) -> List[str]:
    """
    Recursively walk through all of the dataset files in the given directory and return a list of
    file names for the language files, containing the full path to the file.
    """
    filenames = []

    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(file_type):
                if any([split in f for split in splits]):
                    filenames.append(os.path.join(root, f))

    return filenames


def parse_language_code_from_filename(filename: str) -> str:
    """
    Parses the language name from the file name where the file name
    matches a format similar to:

    gs://c4ai-instruct-multilingual-data/team3/datasets/CMRC2018/eng_Latn_to_ace_Latn/
    facebook-nllb-200-3.3B/in_an_exam/2023-03-30/train.csv

    The language name is in the "eng_Latn_to_ace_Latn" part of the file name, following
    the "to_" string and before the "Latn" string.
    """
    language_name = filename.split("to_")[1].split("_")[0]
    return language_name


def parse_character_code_from_filename(filename: str) -> str:
    """
    Similar to parsing language code except get the character code,
    which comes after "to_<language>" and before "/<model>".
    """
    character_code = filename.split("to_")[1].split("_")[1].split('/')[0]
    return character_code


def get_language_id_for_matching_codes(
    language_code: str,
    character_code: str,
) -> str:
    """
    Returns the language ID for the language with the given name.
    """
    statement = sa.select(
        [language_table.c.id]
    ).where(
        language_table.c.code == language_code
    ).where(
        language_table.c.character_code == character_code
    )

    results = connection.execute(statement).fetchone()

    if results is not None:
        language_id = results[0]
    else:
        language_id = None

    return language_id


def insert_dataset(
    name: str,
    language_id: str,
    translated: bool,
    templated: bool,
) -> str:
    """
    Inserts a new dataset into the dataset table and returns the dataset ID.

    Returns the existing dataset_id if the dataset already exists.
    """
    logger.info(f"Inserting new dataset with name {name}...")
    statement = insert(dataset_table).values(
        name=name,
        language_id=language_id,
        translated=translated,
        templated=templated,
    )
    statement = statement.on_conflict_do_nothing(index_elements=["name"])
    result = connection.execute(statement)

    if result.rowcount == 0:
        # The dataset already exists, so get the dataset ID
        statement = sa.select([dataset_table.c.id]).where(dataset_table.c.name == name)
        dataset_id = connection.execute(statement).fetchone()[0]
        logger.info(f"Dataset already exists with ID {dataset_id}")
    else:
        # The dataset was inserted, so get the dataset ID
        dataset_id = result.inserted_primary_key[0]
        logger.debug(f"Inserted new dataset with ID {dataset_id}")

    return dataset_id


def randomly_sample_lines_from_gcp_dataset_file(
    dataset_name: str,
    sample_size: int,
) -> List[Dict[str, str]]:
    """
    Randomly samples a given number of rows from the dataset with the given ID.

    The dataset name can be either a `.jsonl` file or `.csv` file.
    """
    if dataset_name.endswith(".jsonl"):
        return _randomly_sample_lines_from_gcp_dataset_file_jsonl(
            dataset_name, sample_size
        )
    elif dataset_name.endswith(".csv"):
        return _randomly_sample_lines_from_gcp_dataset_file_csv(
            dataset_name, sample_size
        )
    else:
        raise Exception(f"Unrecognized dataset file type: {dataset_name}")


def _randomly_sample_lines_from_gcp_dataset_file_jsonl(
    dataset_name: str,
    sample_size: int,
) -> List[Dict[str, str]]:
    """
    Randomly samples a given number of rows from the dataset with the given ID.
    """
    # Read the entire file into memory
    with open(dataset_name, "r", encoding="utf-8") as f:
        lines = f.readlines()

    logger.debug(
        f"Randomly sampling {sample_size} lines from {dataset_name} (total lines: {len(lines)})"
    )

    # Sample (if possible)
    if len(lines)>=sample_size:
        # Randomly sample the given number of lines
        sample = random.sample(lines, sample_size)
    else:
        sample = lines

    # Convert the sample to a list of dictionaries
    # Replace the NULL character since it doesn't play well with PostgreSQL
    sample = [json.loads(line.replace('\\u0000','')) for line in sample]

    return sample


def _randomly_sample_lines_from_gcp_dataset_file_csv(
    dataset_name: str,
    sample_size: int,
) -> List[Dict[str, str]]:
    """
    Randomly samples a given number of rows from the dataset with the given ID.
    """
    # Read the entire file into memory
    with open(dataset_name, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        lines = list(reader)

    logger.info(
        f"Randomly sampling {sample_size} lines from {dataset_name} (total lines: {len(lines)})"
    )

    # Randomly sample the given number of lines
    sample = random.sample(lines, sample_size)
    return sample


def _add_full_dataset(dataset_name: str):
    """
    Adds all of the rows from the dataset with the given ID.

    The dataset name can be either a `.jsonl` file or `.csv` file.
    """
    if dataset_name.endswith(".jsonl"):
        return _add_full_gcp_dataset_file_jsonl(
            dataset_name,
        )
    elif dataset_name.endswith(".csv"):
        return _add_full_gcp_dataset_file_csv(
            dataset_name,
        )
    else:
        raise Exception(f"Unrecognized dataset file type: {dataset_name}")


def _add_full_gcp_dataset_file_jsonl(dataset_name: str):
    # Read the entire file into memory
    with open(dataset_name, "r", encoding="utf-8") as f:
        lines = f.readlines()

    logger.debug(
        f"Adding all lines from {dataset_name} (total lines: {len(lines)})"
    )

    # Convert the data to a list of dictionaries

    # Replace the NULL character since it doesn't play well with PostgreSQL
    sample = [json.loads(line.replace('\\u0000','')) for line in lines]
    return sample


def _add_full_gcp_dataset_file_csv(dataset_name: str):
    # Read the entire file into memory
    with open(dataset_name, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        lines = list(reader)

    logger.info(
        f"Adding all lines from {dataset_name} (total lines: {len(lines)})"
    )

    return lines


def send_discord_webhook_message(
    discord_url: str,
    message: str,
    dry_run: bool,
    embeds: Optional[List[str]] = None,
):
    """
    Sends a message to a discord webhook.
    """
    if dry_run:
        logger.info("dry run enabled. skipping discord message...")
        return
    
    # send a message to a discord webhook
    # and use the default username and avatar
    data = {"content" : message}

    if embeds is not None:
        data["embeds"] = embeds

    logger.info(f"sending discord webhook message...")

    # time the request
    start_time = time.time()

    response = requests.post(
        discord_url,
        json=data,
    )

    elapsed_time = time.time() - start_time

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.error(err)
    else:
        logger.info(
            f"payload took {elapsed_time:.2f} seconds with status code {response.status_code}"
        )


@click.command(context_settings={'show_default': True})
@click.option(
    "--dataset-dir",
    help="The directory containing the datasets",
    type=str,
    required=True,
)
@click.option(
    "--sample-size",
    default=1000,
    help="The number of lines to sample from each dataset file",
    type=int,
    required=False,
)
@click.option(
    "--add-full-dataset",
    help="Whether or not to add an entire dataset to the database",
    required=False,
    is_flag=True,
)
@click.option(
    "--task-type",
    help="The type of task to create",
    type=click.Choice(["audit_translation", "audit_xp3", "audit_crowdsourced_data"]),
    required=True,
)
@click.option(
    "--splits",
    help=(
        "The splits to load into the database. Can specify more than one."
        'Use "all" to load all splits.'
    ),
    type=click.Choice(["train", "validation", "test", "all"]),
    multiple=True,
    required=True,
)
@click.option(
    "--file-type",
    help="The type of file to load",
    type=click.Choice(["jsonl", "csv"]),
    required=True,
)
@click.option(
    "--translated",
    help="Whether the dataset was translated by C4AI",
    is_flag=True,
)
@click.option(
    "--templated",
    help="Whether the dataset was generated using a template",
    is_flag=True,
)
@click.option(
    "--prompt-key",
    default="inputs",
    help=(
        'Key to read in .jsonl files that maps to the prompt value. "'
        'e.g. {"meaning_representation": <prompt>}'
    ),
    required=False,
)
@click.option(
    "--completion-key",
    default="targets",
    help=(
        'Key to read in .jsonl files that maps to the completion value. "'
        'e.g. {"human_reference": <completion>}'
    ),
    required=False,
)
@click.option(
    "--dry-run",
    help="Whether to perform a dry run (i.e. do not insert into the database)",
    is_flag=True,
)
def main(
    dataset_dir: str,
    sample_size: int,
    add_full_dataset: bool,
    task_type: str,
    splits: List[str],
    file_type: str,
    translated: bool,
    templated: bool,
    prompt_key: str,
    completion_key: str,
    dry_run: bool,
):
    if add_full_dataset and sample_size!=1000:
        raise Exception(
            'You cannot add a full dataset and also select a sample size. '
            'Please use one of --add-full-dataset or --sample-size'
        )

    if "all" in splits:
        all_splits = ["train", "validation", "test"]

    if dry_run:
        logger.info("Performing a dry run (no database inserts will be performed)")

    dirname = (Path(__file__).parent / Path(dataset_dir)).as_posix()

    logger.info(f"Loading datasets from {dirname}")

    gcp_files = get_gcp_language_filenames(
        directory=dirname,
        splits=all_splits,
        file_type=file_type,
    )
    logger.info(f"Found {len(gcp_files)} files")

    failed_inserts = []
    skipped_datasets = []
    skipped_languages = []

    start = time.time()
    for dataset_name in gcp_files:
        shortname = "/".join(dataset_name.split("/")[6:])

        logger.info(f"Processing dataset {shortname}")

        try:
            language_code = parse_language_code_from_filename(dataset_name)
        except Exception as e:
            logger.warning(
                f"Could not parse language code from filename {shortname}. "
                "Ensure that the file has <from_language>_<char_code>_to_<to_language>_<char_code>. "
                "Skipping..."
            )
            skipped_datasets.append((dataset_name, e))
            continue


        try:
            character_code = parse_character_code_from_filename(dataset_name)
        except Exception as e:
            logger.warning(
                f"Could not parse character code from filename {shortname}. "
                "Ensure that the file has <from_language>_<char_code>_to_<to_language>_<char_code>. "
                "Skipping..."
            )
            skipped_datasets.append((dataset_name, e))
            continue

        language_id = get_language_id_for_matching_codes(
            language_code=language_code,
            character_code=character_code,
        )

        if language_id is None:
            logger.warning(
                f"No language found for language_code {language_code}. "
                f"and character_code {character_code}. Skipping..."
            )
            skipped_languages.append(language_code)
            continue

        dataset_id = insert_dataset(
            name=dataset_name,
            language_id=language_id,
            translated=translated,
            templated=templated,
        )

        if not add_full_dataset:
            samples = randomly_sample_lines_from_gcp_dataset_file(
                dataset_name,
                sample_size=sample_size,
            )
        else:
            samples = _add_full_dataset(dataset_name)

        task_data = []
        for sample in samples:
            if dataset_name.endswith(".jsonl"):
                prompt = sample[prompt_key]
                completion = sample[completion_key]
            elif dataset_name.endswith(".csv"):
                prompt = sample[0]
                completion = sample[1]
            else:
                raise Exception(f"Unrecognized dataset file type: {dataset_name}")

            task_data.append(
                {
                    "task_type": task_type,
                    "dataset_id": dataset_id,
                    "language_id": language_id,
                    "prompt": prompt,
                    "completion": completion,
                }
            )

        logger.debug(
            f"attempting to insert tasks for dataset {dataset_name} (dataset_id: {dataset_id})"
        )

        # try to insert the tasks and on conflict do nothing if the task already exists
        # based on the hash. this is to prevent duplicate tasks from being inserted.
        # return the ids of the inserted tasks
        statement = insert(task_table).values(task_data)
        statement = statement.on_conflict_do_nothing(
            index_elements=["key_hash"]
        ).returning(task_table.c.id)

        discord_message_parts = []
        username = getpass.getuser()

        message_start_part = (
            "Dataset upload process was run by "
            f"`{username}` at {datetime.datetime.utcnow()} UTC"
        )
        discord_message_parts.append(message_start_part)
        discord_message_parts.append("")

        try:
            inserted_rows = connection.execute(statement).fetchall()

            if dry_run:
                logger.info(
                    f"Would have inserted {len(inserted_rows)} tasks for dataset {shortname}"
                )
                continue
            else:
                connection.commit()
        except Exception as e:
            logger.warning(f'Could not insert rows for dataset {shortname}. Storing error for summary...')
            connection.rollback()
            failed_inserts.append((dataset_name, e))
        else:
            insert_message_part = (
                f"Inserted {len(inserted_rows)} {task_type} tasks for:\ndataset: `{shortname}`, "
                f"\nlanguage_id `{language_id}`\nlanguage code `{language_code}`"
            )
            logger.info(insert_message_part)
            discord_message_parts.append(insert_message_part)
            discord_message_parts.append("")

    report_header_part = "----------------- SUCCESS / FAILURE REPORT -----------------"
    logger.info("\n")
    logger.info(report_header_part)
    discord_message_parts.append(report_header_part)

    if skipped_datasets:
        skipped_datasets_part = pformat(f"Skipped datasets with reasons: {skipped_datasets}")
        logger.info(skipped_datasets_part)
        discord_message_parts.append(skipped_datasets_part)
        discord_message_parts.append("")
    else:
        skipped_datasets_part = "No skipped datasets. 100% Success!"
        logger.info(skipped_datasets_part)
        discord_message_parts.append(skipped_datasets_part)

    if skipped_languages:
        skipped_languages_part = pformat(
            f"Skipped languages due to no matching language in DB: {set(skipped_languages)}"
        )
        logger.info(skipped_languages_part)
        discord_message_parts.append(skipped_languages_part)
        discord_message_parts.append("")
    else:
        skipped_languages_part = "No skipped languages. 100% Success!"
        logger.info(skipped_languages_part)
        discord_message_parts.append(skipped_languages_part)

    if failed_inserts:
        failed_inserts_part = pformat(f"Failed inserts with reasons: {failed_inserts}")
        logger.info(failed_inserts_part)
        discord_message_parts.append(failed_inserts_part)
        discord_message_parts.append("")
    else:
        failed_inserts_part = "No failed inserts for successful datasets. 100% Success!"
        logger.info(failed_inserts_part)
        discord_message_parts.append(failed_inserts_part)

    processing_part = f"\nProcessing took: `{time.time() - start}` seconds"
    logger.info(processing_part)
    discord_message_parts.append(processing_part)

    discord_message = "\n".join(discord_message_parts)
    send_discord_webhook_message(
        discord_url=discord_webhook_url,
        message=discord_message,
        dry_run=dry_run,
    )


if __name__ == "__main__":
    from sqlalchemy.pool import NullPool

    logger.info(f"Establishing database connection...")
    engine = sa.create_engine(
        db_uri,
        client_encoding="utf8",
        future=True,
        poolclass=NullPool,
    )
    language_table = sa.Table(
        "language_code",
        sa.MetaData(),
        autoload=True,
        autoload_with=engine,
    )
    dataset_table = sa.Table(
        "dataset",
        sa.MetaData(),
        autoload=True,
        autoload_with=engine,
    )
    task_table = sa.Table(
        "task",
        sa.MetaData(),
        autoload=True,
        autoload_with=engine,
    )

    with engine.connect() as connection:
        logger.info(f"Connected to database.")
        main()

"""
Script that connects to the local database and then seeds it with fake data.

Creates a user with an two assigned language codes, and a country code.

Also adds a fake dataset along with some tasks that are mapped to the dataset.
"""

import logging
import os
from typing import List

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, create_engine

from instruct_multilingual.models import TaskContribution, TaskAudit
from instruct_multilingual.models.country_code import CountryCode
from instruct_multilingual.models.dataset import Dataset
from instruct_multilingual.models.language_code import LanguageCode
from instruct_multilingual.models.task import Task
from instruct_multilingual.models.user import User

load_dotenv('.env.local')

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

engine = create_engine(
    os.environ['INSTRUCT_MULTILINGUAL_APP_DB_URI'],
    client_encoding="utf8",
    # Applications using this level must be prepared to retry transactions due to serialization failures.
    isolation_level="REPEATABLE READ",
)


def get_language_code() -> LanguageCode:
    """
    Gets a language code to assign to the user.
    """
    with Session(engine) as session:
        statement = (
            select(LanguageCode)
            .where(LanguageCode.code == "spa")
        )

        language_code = session.execute(statement).one()[0]

    return language_code


def get_country_code() -> CountryCode:
    """
    Gets a country code to assign to the user.
    """
    with Session(engine) as session:
        statement = (
            select(CountryCode)
            .where(CountryCode.code == "ES")
        )

        country_code = session.execute(statement).one()[0]

    return country_code


def create_user(language_code: LanguageCode, country_code: CountryCode) -> User:
    """
    Creates a new user.
    """
    with Session(engine) as session:
        statement = (
            insert(User)
            .values(
                username="test_user",
                image_url="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png",
                language_codes=[language_code.id],
                country_code=country_code.id,
                email="testuser@gmail.com",
                discord_id="1234567890",
                google_id="1234567890",
            )
            .returning(User)
        )

        user = session.execute(statement).one()
        session.commit()

    return user


def create_dataset(language_code: LanguageCode) -> Dataset:
    """
    Creates a dataset that can be mapped to tasks
    """
    with Session(engine) as session:
        statement = (
            insert(Dataset)
            .values(
                name="test_dataset",
                language_id=language_code.id,
                translated=False,
                templated=True,
            )
            .on_conflict_do_update(
                index_elements=["name"],
                set_=dict(
                    name="test_dataset",
                    language_id=language_code.id,
                    translated=False,
                    templated=True,
                ),
            )
            .returning(Dataset)
        )

        dataset = session.execute(statement).one()
        session.commit()

    return dataset


def create_tasks(dataset: Dataset) -> List[Task]:
    """
    Creates tasks for the given dataset.
    """
    fake_tasks = [
        {
            "prompt": "This is a test prompt",
            "completion": "This is a test completion",
            "task_type": "audit_xp3",
            "dataset_id": dataset.id,
            "language_id": dataset.language_id,
        },
        {
            "prompt": "Termina la siguiente oración con la mejor opción: Agregar agarre adicional para quitar el frasco. Opciones: - Coloque la almohadilla caliente de silicona sobre la tapa. - Coloque la almohadilla caliente de silicona debajo del frasco. Respuesta:",
            "completion": "Coloque una almohadilla caliente de silicona sobre la tapa.",
            "task_type": "audit_translation",
            "dataset_id": dataset.id,
            "language_id": dataset.language_id,      
        },
    ]

    for i in range(1, 100):
        fake_tasks.append({
            "prompt": f"This is test prompt {i}",
            "completion": f"This is test completion {i}",
            "task_type": "audit_xp3",
            "dataset_id": dataset.id,
            "language_id": dataset.language_id,
        },
    )

    data = []
    with Session(engine) as session:
        for ft in fake_tasks:
            statement = (
                insert(Task)
                .values(ft)
                .on_conflict_do_nothing(
                    index_elements=["key_hash"],
                )
                .returning(Task)
            )
            tasks = session.execute(statement).one_or_none()
            if tasks:
                data.append(tasks)

        session.commit()

    return data


def create_task_audits(user: User, tasks: List[Task]) -> List[TaskAudit]:
    """
    Creates task audits for the given dataset.
    """
    task_audits = []
    for task in tasks:
        task_audits.append({
            "task_id": task.id,
            "submitted_by": user.id,
            "submitted_prompt": task.prompt + " (edited)",
            "submitted_completion": task.completion + " (edited)",
            "prompt_edited": True,
            "completion_edited": True,
            "prompt_rating": 0,
            "completion_rating": 0,
        },
    )

    data = []
    with Session(engine) as session:
        for ta in task_audits:
            statement = (
                insert(TaskAudit)
                .values(ta)
                .on_conflict_do_nothing(
                    index_elements=["id"],
                )
                .returning(TaskAudit)
            )
            tasks = session.execute(statement).one_or_none()
            if tasks:
                data.append(tasks)

        session.commit()

    return data


def create_task_contribution(user: User, dataset: Dataset) -> List[TaskContribution]:
    """
    Creates contributions for the given dataset.
    """
    fake_tasks = []
    for i in range(1, 100):
        fake_tasks.append({
            "submitted_by": user.id,
            "submitted_prompt": f"This is a contributed prompt {i}",
            "submitted_completion": f"This is contributed completion {i}",
            "language_id": dataset.language_id,
        },
    )

    data = []
    with Session(engine) as session:
        for ft in fake_tasks:
            statement = (
                insert(TaskContribution)
                .values(ft)
                .on_conflict_do_nothing(
                    index_elements=["id"],
                )
                .returning(TaskContribution)
            )
            tasks = session.execute(statement).one_or_none()
            if tasks:
                data.append(tasks)

        session.commit()

    return data


def main() -> None:
    """
    Main function.
    """
    logger.info("Seeding database with fake data...")

    language_code = get_language_code()
    country_code = get_country_code()

    user = create_user(language_code, country_code)
    dataset = create_dataset(language_code)
    tasks = create_tasks(dataset)
    task_audits = create_task_audits(user, tasks)
    task_contributions = create_task_contribution(user, dataset)

    logger.info("Done!")

    logger.info(f"Created the following user: {user}")
    logger.info(f"Created the following language code: {language_code}")
    logger.info(f"Created the following dataset: {dataset}")
    logger.info(f"Created the following task_audits: {task_audits}")
    logger.info(f"Created the following task_contributions: {task_contributions}")


if __name__ == "__main__":
    main()

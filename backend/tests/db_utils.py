from sqlmodel import select

from instruct_multilingual.models import (
    Dataset,
    LanguageCode,
    Task,
    TaskContribution,
    User,
)


def populate_db_with_datasets(database):
    language_codes = database.exec(select(LanguageCode)).all()

    datasets = []
    for i in range(len(language_codes)):
        # create a dataset for each language code
        dataset = Dataset(
            name=f"test dataset {i}",
            language_id=language_codes[i].id,
            translated=True,
            templated=True,
        )
        database.add(dataset)
        database.commit()
        database.refresh(dataset)
        datasets.append(dataset)

    return datasets


def populate_db_with_tasks(database):
    populate_db_with_datasets(database)

    datasets = database.exec(select(Dataset)).all()

    tasks = []
    for i in range(len(datasets)):
        # create a task for each dataset
        task = Task(
            prompt=f"test prompt {i}",
            completion=f"test completion {i}",
            dataset_id=datasets[i].id,
            task_type="audit_translation",
            language_id=datasets[i].language_id,
        )
        database.add(task)
        database.commit()
        database.refresh(task)
        tasks.append(task)

    return tasks


def clear_tasks_from_db(database):
    tasks = database.exec(select(Task)).all()

    for task in tasks:
        database.delete(task)
        database.commit()

    return tasks


def get_one_task_from_db(database):
    task = database.exec(select(Task)).first()
    return task


def get_all_tasks_from_db(database):
    tasks = database.exec(select(Task)).all()
    return tasks


def populate_db_with_users(database, prefix=0):
    users = []
    for i in range(3):
        user = User(
            username=f"test user {i}",
            email=f"testemail{prefix}{i}@fake-aya-mail.com",
            image_url=f"test image url {i}",
        )
        database.add(user)
        database.commit()
        database.refresh(user)
        users.append(user)

    return users


def clear_users_from_db(database):
    users = database.exec(select(User)).all()

    for user in users:
        database.delete(user)
        database.commit()

    return users


def get_all_users_from_db(database):
    users = database.exec(select(User)).all()
    return users


def get_all_task_contributions_from_db(database):
    task_contributions = database.exec(select(TaskContribution)).all()
    return task_contributions

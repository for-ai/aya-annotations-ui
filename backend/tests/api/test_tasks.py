import uuid

from tests.api_utils import responses_sameshape
from tests.db_utils import (
    get_all_tasks_from_db,
    get_all_users_from_db,
    get_all_task_contributions_from_db,
    populate_db_with_tasks,
    populate_db_with_users, )


def test_get_tasks(test_client, db):
    tasks = populate_db_with_tasks(db)

    user_id = uuid.uuid4()
    language_id = tasks[0].language_id

    response = test_client.get(
        f"/api/v1/tasks?user_id={user_id}&language_id={language_id}"
    )
    assert response.status_code == 200

    actual_data = response.json()
    expected_data = {
        "tasks": [
            {
                "id": "1",
                "prompt": "test prompt 0",
                "completion": "test completion 0",
                "is_contributed": False,
            },
        ],
    }
    assert responses_sameshape(actual_data, expected_data)


def test_get_tasks_contributed(test_client, db):
    tasks = get_all_tasks_from_db(db)
    user_id = uuid.uuid4()
    language_id = tasks[0].language_id

    # get a user from the DB
    users = populate_db_with_users(db)
    user = users[0]
    user_id = user.id

    # add a user contribution
    response = test_client.post(
        "/api/v1/tasks/submit-contribution",
        json={
            "submitted_by": str(user_id),
            "language_id": str(language_id),
            "submitted_prompt": "test prompt",
            "submitted_completion": "test completion",
        }
    )
    assert response.status_code == 201

    contribution_id = response.json()["id"]

    # get the tasks
    response = test_client.get(
        f"/api/v1/tasks?user_id={user_id}&language_id={language_id}"
    )
    assert response.status_code == 200

    actual_data = response.json()
    expected_data = {
        "tasks": [
            {
                "id": contribution_id,
                "prompt": "test prompt",
                "completion": "test completion",
                "is_contributed": True,
            },
        ],
    }
    assert responses_sameshape(actual_data, expected_data)


def test_get_tasks_contributed_then_audit(test_client, db):
    tasks = get_all_tasks_from_db(db)
    user_id = uuid.uuid4()
    language_id = tasks[0].language_id

    # get a user from the DB
    users = populate_db_with_users(db, prefix=1)
    user = users[0]
    user_id = user.id

    # add a user contribution
    response = test_client.post(
        "/api/v1/tasks/submit-contribution",
        json={
            "submitted_by": str(user_id),
            "language_id": str(language_id),
            "submitted_prompt": "test prompt",
            "submitted_completion": "test completion",
        }
    )
    assert response.status_code == 201

    contribution_id = response.json()["id"]

    # get the tasks
    response = test_client.get(
        f"/api/v1/tasks?user_id={user_id}&language_id={language_id}"
    )
    assert response.status_code == 200

    actual_data = response.json()
    expected_data = {
        "tasks": [
            {
                "id": contribution_id,
                "prompt": "test prompt",
                "completion": "test completion",
                "is_contributed": True,
            },
        ],
    }
    assert responses_sameshape(actual_data, expected_data)

    contribution_prompt = response.json()["tasks"][0]["prompt"]
    contribution_completion = response.json()["tasks"][0]["completion"]

    # then audit that contribution
    # then, submit an audit for the task
    response = test_client.post(
        "/api/v1/tasks/submit-contribution-audit",
        json={
            "task_contribution_id": contribution_id,
            "submitted_by": str(user_id),
            "submitted_prompt": contribution_prompt,
            "submitted_completion": contribution_completion,
            "prompt_edited": False,
            "completion_edited": False,
            "prompt_rating": 1,
            "completion_rating": 1
        }
    )
    assert response.status_code == 201


def test_get_tasks_one_less_after_audit(test_client, db):
    """
    Ensure that we get one less task for a user after we audit one.
    """
    # get a task from the DB
    tasks = get_all_tasks_from_db(db)
    task = tasks[1]
    language_id = task.language_id

    # get a user from the DB
    users = get_all_users_from_db(db)
    user = users[1]
    user_id = user.id

    # first, ensure we can get a task from the DB
    # and we should get a 200 response
    response = test_client.get(
        f"/api/v1/tasks?user_id={user_id}&language_id={language_id}"
    )
    assert response.status_code == 200

    # then, submit an audit for the task
    response = test_client.post(
        "/api/v1/tasks/submit-audit",
        json={
            "task_id": str(task.id),
            "submitted_by": str(user.id),
            "submitted_prompt": task.prompt,
            "submitted_completion": task.completion,
            "prompt_edited": False,
            "completion_edited": False,
            "prompt_rating": 1,
            "completion_rating": 1
        }
    )
    assert response.status_code == 201

    # finally, try and get a task from the DB again.
    # we should get a 204 response, because we've already audited
    # all the tasks in the database that this user can audit
    # for the given language
    response = test_client.get(
        f"/api/v1/tasks?user_id={user_id}&language_id={language_id}"
    )
    assert response.status_code == 204


def test_get_tasks_when_no_tasks_available(test_client, db):
    """
    Ensure that we get a 204 response when there are no tasks available.
    In this particular case, we'll test for when all tasks have been audited
    for a given language 3 times by other users, meaning that for a particular
    user, there are no tasks available.
    """
    # get a task from the DB
    tasks = get_all_tasks_from_db(db)
    task = tasks[1]
    language_id = task.language_id

    # get two users from the DB
    users = populate_db_with_users(db, prefix=2)
    current_user = users[0]
    other_user = users[1]

    current_user_id = current_user.id

    # first, ensure we can get a task from the DB
    # and we should get a 200 response
    response = test_client.get(
        f"/api/v1/tasks?user_id={current_user_id}&language_id={language_id}"
    )
    assert response.status_code == 200

    # then, submit an audit for every task with this language_id 3 times
    # by other users
    for task in tasks:
        if task.language_id == language_id:
            for i in range(3):
                response = test_client.post(
                    "/api/v1/tasks/submit-audit",
                    json={
                        "task_id": str(task.id),
                        "submitted_by": str(other_user.id),
                        "submitted_prompt": task.prompt,
                        "submitted_completion": task.completion,
                        "prompt_edited": False,
                        "completion_edited": False,
                        "prompt_rating": 1,
                        "completion_rating": 1
                    }
                )
                assert response.status_code == 201

    # finally, try and get a task from the DB again.
    # we should get a 204 response, because we've already audited
    # all the tasks in the database that this user can audit
    # for the given language
    response = test_client.get(
        f"/api/v1/tasks?user_id={current_user_id}&language_id={language_id}"
    )
    assert response.status_code == 204


def test_get_tasks_with_invalid_user_id(test_client):
    user_id = "invalid"
    language_id = uuid.uuid4()

    response = test_client.get(
        f"/api/v1/tasks?user_id={user_id}&language_id={language_id}"
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "user_id"],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid",
            }
        ]
    }


def test_get_tasks_with_invalid_language_code(test_client):
    user_id = uuid.uuid4()
    language_id = "invalid uuid"

    response = test_client.get(
        f"/api/v1/tasks?user_id={user_id}&language_id={language_id}"
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "language_id"],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid",
            }
        ]
    }


def test_get_tasks_with_missing_user_id(test_client):
    language_id = uuid.uuid4()

    response = test_client.get(f"/api/v1/tasks?language_id={language_id}")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "user_id"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_get_tasks_with_missing_language_id(test_client):
    user_id = uuid.uuid4()

    response = test_client.get(f"/api/v1/tasks?user_id={user_id}")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "language_id"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_get_tasks_with_missing_user_id_and_language_id(test_client):
    response = test_client.get(f"/api/v1/tasks")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "user_id"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["query", "language_id"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_submit_task_contribution_audit(test_client, db):
    task_contributions = get_all_task_contributions_from_db(db)
    contribution_id = task_contributions[0].id

    user_id = task_contributions[0].submitted_by

    response = test_client.post(
        "/api/v1/tasks/submit-contribution-audit",
        json={
            "task_contribution_id": str(contribution_id),
            "submitted_by": str(user_id),
            "submitted_prompt": "test prompt",
            "submitted_completion": "test completion",
            "prompt_edited": True,
            "completion_edited": True,
            "prompt_rating": 0,
            "completion_rating": 0
        }
    )
    assert response.status_code == 201


def test_submit_task_contribution_with_empty_prompt_completion(test_client):
    user_id = uuid.uuid4()
    language_id = uuid.uuid4()

    response = test_client.post(
        "/api/v1/tasks/submit-contribution",
        json={
            "submitted_by": str(user_id),
            "submitted_prompt": "",
            "submitted_completion": "",
            "language_id": str(language_id),
        }
    )
    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "submitted_prompt"],
                "msg": "prompt must not be empty",
                "type": "value_error"
            },
            {
                "loc": ["body", "submitted_completion"],
                "msg": "completion must not be empty",
                "type": "value_error"
            }
        ]
    }

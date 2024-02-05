import logging
import random
from uuid import UUID

from fastapi import APIRouter, Response, status

from instruct_multilingual.exceptions import (
    InstructMultilingualAPIError,
    IDNotFoundError,
)
from instruct_multilingual.services import (
    TaskService,
    TaskAuditService,
    TaskContributionService,
    TaskAuditReviewService,
    TaskContributionAuditReviewService,
)
from instruct_multilingual.schemas.task import (
    TaskSchema,
    TaskListSchema,
    TaskAuditRequestSchema,
    TaskAuditResponseSchema,
    TaskAuditGetResponseSchema,
    TaskAuditGetResponseListSchema,
    TaskContributionRequestSchema,
    TaskContributionResponseSchema,
    TaskContributionAuditRequestSchema,
    TaskContributionAuditResponseSchema,
    TaskAuditReviewRequestSchema,
    TaskAuditReviewResponseSchema,
    TaskContributionAuditReviewRequestSchema,
    TaskContributionAuditReviewResponseSchema,
)

MAX_TASKS = 20

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

router = APIRouter()

audit_service = TaskAuditService()
contribution_service = TaskContributionService()
task_service = TaskService()
task_audit_review_service = TaskAuditReviewService()
contribution_audit_review_service = TaskContributionAuditReviewService()


@router.get(
    "/",
    response_model=TaskListSchema,
    status_code=status.HTTP_200_OK,
)
def get_tasks(
    *,
    user_id: UUID,
    language_id: UUID,
):
    """
    Returns a list of tasks for a given language and user.

    Tasks are first pulled from the `task_contribution` table. If there are no tasks,
    then tasks are pulled from the `task` table.

    Tasks from the `task` table are tasks the Aya team have created through translation
    or through existing xP3 data.

    Tasks from the `task_contribution` table are tasks
    that have been contributed by users, and we want to prioritize these tasks over
    tasks from the `task` table, to ensure that we are getting feedback on the
    quality of user contributions.
    """
    task_queue = []

    try:
        contributed_tasks = contribution_service.get_task_contributions_for_user_and_language_id(
            user_id=user_id,
            language_id=language_id,
        )
    except Exception as e:
        logger.error(e)
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="an error occurred while retrieving tasks.",
        )

    # if there are task contributions, add them to the list
    # of tasks we want to return
    for task_contribution in contributed_tasks:
        task = TaskSchema(
            id=task_contribution.id,
            prompt=task_contribution.submitted_prompt,
            completion=task_contribution.submitted_completion,
            is_contributed=True,
        )
        task_queue.append(task)

    # if we haven't filled up our queue to the max,
    # add generated tasks to fill it
    num_to_fill = MAX_TASKS - len(task_queue)
        
    # otherwise, return `diff` tasks from the task table
    try:
        generated_tasks = task_service.get_active_tasks_for_user_and_language_id(
            user_id=user_id,
            language_id=language_id,
            num_tasks=num_to_fill,
        )
    except Exception as e:
        logger.error(e)
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="an error occurred while retrieving tasks.",
        )

    for generated_task in generated_tasks:
        task = TaskSchema(
            id=generated_task.id,
            prompt=generated_task.prompt,
            completion=generated_task.completion,
            is_contributed=False,
        )
        task_queue.append(task)

    # and if we have no tasks at all, 204
    if not task_queue:
        logger.debug(
            f"no tasks available for language id {language_id} and user {user_id}",
        )
        # see: https://github.com/tiangolo/fastapi/issues/717
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    task_list = TaskListSchema(
        tasks=task_queue,
    )
    return task_list


@router.get(
    "/audits",
    response_model=TaskAuditGetResponseListSchema,
    status_code=status.HTTP_200_OK,
)
def get_task_audits(
    *,
    user_id: UUID,
    language_id: UUID,
):
    """
    Returns a list of task audits for a given language and user,
    pulling from the `task_audit` and `task_contribution_audit` tables.
    """
    try:
        task_audits = audit_service.get_task_audits_for_user_and_language_id(
            user_id=user_id,
            language_id=language_id,
        )
    except Exception as e:
        logger.error(e)
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="an error occurred while retrieving task audits.",
        )

    # if we have no task audits at all, 204
    if not task_audits:
        logger.debug(
            f"no task audits available for language id {language_id} and user {user_id}",
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # map the task audit records to the response schema
    task_audit_list = [
        TaskAuditGetResponseSchema(
            id=task_audit.id,
            contributed_by_id=task_audit.user_id,
            contributed_by=task_audit.username,
            contributed_by_image=task_audit.image_url,
            original_prompt=task_audit.prompt,
            original_completion=task_audit.completion,
            edited_prompt=task_audit.submitted_prompt,
            edited_completion=task_audit.submitted_completion,
            is_contributed=task_audit.is_contributed,
        )
        for task_audit in task_audits
    ]

    return TaskAuditGetResponseListSchema(
        task_audits=task_audit_list,
    )


@router.post(
    "/submit-audit",
    response_model=TaskAuditResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def submit_task_audit(audit: TaskAuditRequestSchema):
    """
    Creates a new task audit.
    """
    try:
        task_audit = audit_service.create_task_audit(**audit.dict())
    except IDNotFoundError as e:
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(e)
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"an error occurred while submitting task {audit.task_id}.",
        )

    return task_audit


@router.post(
    "/submit-contribution",
    response_model=TaskContributionResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def submit_task_contribution(contribution: TaskContributionRequestSchema):
    """
    Creates a new task contribution.
    """
    try:
        task_contribution = contribution_service.create_task_contribution(
            **contribution.dict(),
        )
    except Exception as e:
        logger.error(e)
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "an error occurred while submitting task contribution from user "
                f"{contribution.submitted_by}."
            ),
        )

    return task_contribution


@router.post(
    "/submit-contribution-audit",
    response_model=TaskContributionAuditResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def submit_task_contribution_audit(
    contribution_audit: TaskContributionAuditRequestSchema,
):
    """
    Creates a new task contribution.
    """
    try:
        task_contribution = contribution_service.create_task_contribution_audit(
            **contribution_audit.dict(),
        )
    except Exception as e:
        logger.error(e)
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "an error occurred while submitting task contribution from user "
                f"{contribution_audit.submitted_by}."
            ),
        )

    return task_contribution


@router.post(
    "/submit-audit-review",
    response_model=TaskAuditReviewResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def submit_task_audit_review(
    audit_review: TaskAuditReviewRequestSchema,
):
    """
    Creates a new task audit review.
    """
    try:
        task_audit_review = task_audit_review_service.create_task_audit_review(
            **audit_review.dict(),
        )
    except Exception as e:
        logger.error(e)
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "an error occurred while submitting task audit review "
                f"for audited task id {audit_review.task_audit_id}."
            ),
        )

    return task_audit_review


@router.post(
    "/submit-contribution-audit-review",
    response_model=TaskContributionAuditReviewResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def submit_task_contribution_audit_review(
    contribution_audit_review: TaskContributionAuditReviewRequestSchema,
):
    """
    Creates a new contribution audit review.
    """
    try:
        task_contribution_audit_review = contribution_audit_review_service.create_task_contribution_audit_review(
            **contribution_audit_review.dict(),
        )
    except Exception as e:
        logger.error(e)
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "an error occurred while submitting task contribution audit review "
                f"for audited task id {contribution_audit_review.task_contribution_audit_id}."
            ),
        )

    return task_contribution_audit_review

import logging
import random
from typing import List, Union
from uuid import UUID

from sqlalchemy import exc as sa_errors
from sqlmodel import Session

from instruct_multilingual import db
from instruct_multilingual.exceptions import IDNotFoundError
from instruct_multilingual.models import TaskAudit, TaskContributionAudit

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

class TaskAuditService:

    def create_task_audit(
        self,
        *,
        task_id: UUID,
        submitted_prompt: str,
        submitted_completion: str,
        submitted_by: UUID,
        prompt_edited: bool,
        completion_edited: bool,
        prompt_rating: int,
        completion_rating: int,
    ) -> TaskAudit:
        """
        Create a task audit.
        """
        try:
            with Session(db.engine) as session:
                task_audit = TaskAudit(
                    task_id=task_id,
                    submitted_prompt=submitted_prompt,
                    submitted_completion=submitted_completion,
                    submitted_by=submitted_by,
                    prompt_edited=prompt_edited,
                    completion_edited=completion_edited,
                    prompt_rating=prompt_rating,
                    completion_rating=completion_rating,
                )
                session.add(task_audit)
                session.commit()
                session.refresh(task_audit)
        except sa_errors.IntegrityError as e:
            message = str(e).lower()

            if "key (task_id)" in message:
                logger.debug(e)
                raise IDNotFoundError(
                    message=f"invalid task id. task {task_audit.task_id} does not exist.",
                )
            elif "key (submitted_by)" in message:
                logger.debug(e)
                raise IDNotFoundError(
                    message=f"invalid user id. user {task_audit.submitted_by} does not exist.",
                )

        return task_audit


    def get_task_audits_for_user_and_language_id(
        self,
        *,
        user_id: UUID,
        language_id: UUID,
    ) -> List[Union[TaskAudit, TaskContributionAudit]]:
        """
        Returns a list of task audits, not created by the user, for a given language.
        """
        query = f"""
        WITH ranked_records AS (
            SELECT
                ta.id,
                u.id as user_id,
                u.username,
                u.image_url,
                t.prompt,
                t.completion,
                ta.submitted_prompt,
                ta.submitted_completion,
                ta.prompt_edited as original_prompt_edited,
                ta.completion_edited as original_completion_edited,
                ta.created_at,
                FALSE AS is_contributed,
                COUNT(*) OVER (PARTITION BY ta.submitted_by) AS audit_count
            FROM task_audit ta
            JOIN task t ON ta.task_id = t.id
            JOIN public.user u ON ta.submitted_by = u.id
            LEFT JOIN task_audit_review tar ON ta.id = tar.task_audit_id
            WHERE tar.task_audit_id IS NULL
            AND ta.submitted_by != '{user_id}'
            AND t.language_id = '{language_id}'
            AND (ta.prompt_edited = TRUE OR ta.completion_edited = TRUE)

            UNION

            SELECT
                tac.id,
                u.id as user_id,
                u.username,
                u.image_url,
                tc.submitted_prompt as prompt,
                tc.submitted_completion as completion,
                tac.submitted_prompt,
                tac.submitted_completion,
                tac.prompt_edited as original_prompt_edited,
                tac.completion_edited as original_completion_edited,
                tac.created_at,
                TRUE AS is_contributed,
                COUNT(*) OVER (PARTITION BY tac.submitted_by) AS audit_count
            FROM task_contribution_audit tac
            JOIN task_contribution tc ON tac.task_contribution_id = tc.id
            JOIN public.user u ON tac.submitted_by = u.id
            LEFT JOIN task_contribution_audit_review tcar ON tac.id = tcar.task_contribution_audit_id
            WHERE tcar.task_contribution_audit_id IS NULL
            AND tac.submitted_by != '{user_id}'
            AND tc.language_id = '{language_id}'
            AND (tac.prompt_edited = TRUE OR tac.completion_edited = TRUE)
        ),
        -- shuffle the records
        shuffled_records AS (
            SELECT
                *,
                ROW_NUMBER() OVER (
                    ORDER BY random()
                ) AS shuffle_num
            FROM ranked_records
        ),
        -- limit the number of records we return to 20
        limited_records AS (
            SELECT *
            FROM shuffled_records
            ORDER BY shuffle_num
            LIMIT 20
        )
        SELECT *
        FROM limited_records
        """
        with Session(db.engine) as session:
            results = session.exec(query).all()

        return results

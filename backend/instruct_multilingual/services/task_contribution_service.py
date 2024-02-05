from uuid import UUID
from typing import List, Optional

from sqlalchemy import text
from sqlmodel import Session

from instruct_multilingual import db
from instruct_multilingual.models import (
    TaskContribution,
    TaskContributionAudit,
)


class TaskContributionService:
    """
    Service for interacting with task contributions.
    """
    def create_task_contribution(
        self,
        *,
        submitted_prompt: str,
        submitted_completion: str,
        submitted_by: UUID,
        language_id: UUID,
    ):
        """
        Creates a task contribution.
        """
        with Session(db.engine) as session:
            task_contribution = TaskContribution(
                submitted_prompt=submitted_prompt,
                submitted_completion=submitted_completion,
                submitted_by=submitted_by,
                language_id=language_id,
            )
            session.add(task_contribution)
            session.commit()
            session.refresh(task_contribution)     

        return task_contribution
    

    def get_task_contributions_for_user_and_language_id(
        self,
        *,
        user_id: UUID,
        language_id: UUID,
    ) -> List[TaskContribution]:
        """
        Returns a list of task contributions for a given language,
        that:

        - have not been audited by the user
        - have not been audited 3 times already
        - have not been contributed by the current user
        """
        task_contributions_query = f"""
        WITH language_tasks AS (
            SELECT
                tc.id,
                tc.submitted_prompt,
                tc.submitted_completion,
                tc.language_id
            FROM task_contribution tc
            -- by doing this left join, we ensure that we only include tasks that have
            -- not been audited by the specific user.
            LEFT JOIN task_contribution_audit tca
                ON (tc.id = tca.task_contribution_id)
                AND tca.submitted_by = '{user_id}'
            JOIN language_code lc
                ON (tc.language_id = lc.id)
            WHERE
              lc.id = '{language_id}'
              AND tca.task_contribution_id IS NULL
              AND tc.submitted_by != '{user_id}'
              -- this is a quick hack to exclude poor contributions from a specific user
              AND tc.submitted_by != '3189d48b-83b3-479e-9395-0130a97dc8c8'
        ),
        task_contribution_audit_counts AS (
            SELECT
                task_contribution_id,
                COUNT(*) AS audit_count
            FROM task_contribution_audit
            GROUP BY task_contribution_id
        )
        SELECT
            id,
            submitted_prompt,
            submitted_completion,
            language_id
        FROM (
            SELECT
                lt.id,
                lt.submitted_prompt,
                lt.submitted_completion,
                lt.language_id,
                ROW_NUMBER() OVER (ORDER BY RANDOM()) AS rownum,
                COALESCE(tcacs.audit_count, 0)
            FROM language_tasks lt
            LEFT JOIN task_contribution_audit_counts tcacs
                ON lt.id = tcacs.task_contribution_id
            WHERE COALESCE(tcacs.audit_count, 0) < 3
                OR tcacs.audit_count IS NULL
        ) AS filtered_task_contributions
        WHERE rownum <= 20;
        """
        with Session(db.engine) as session:
            task_contributions = (
                session.query(TaskContribution)
                .from_statement(text(task_contributions_query))
                .all()
            )

        return task_contributions
    

    def create_task_contribution_audit(
        self,
        *,
        task_contribution_id: UUID,
        submitted_by: UUID,
        submitted_prompt: str,
        submitted_completion: str,
        prompt_edited: bool,
        completion_edited: bool,
        prompt_rating: Optional[int] = None,
        completion_rating: Optional[int] = None,
    ) -> TaskContributionAudit:
        """
        Creates a task contribution audit.
        """
        with Session(db.engine) as session:
            task_contribution_audit = TaskContributionAudit(
                task_contribution_id=task_contribution_id,
                submitted_by=submitted_by,
                submitted_prompt=submitted_prompt,
                submitted_completion=submitted_completion,
                prompt_edited=prompt_edited,
                completion_edited=completion_edited,
                prompt_rating=prompt_rating,
                completion_rating=completion_rating,
            )
            session.add(task_contribution_audit)
            session.commit()
            session.refresh(task_contribution_audit)     

        return task_contribution_audit

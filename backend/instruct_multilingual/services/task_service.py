from uuid import UUID
from typing import List, Optional

from sqlalchemy import text
from sqlmodel import Session

from instruct_multilingual import db
from instruct_multilingual.models import Task

class TaskService:
    """
    Service for interacting with tasks.
    """
    def get_active_tasks_for_user_and_language_id(
        self,
        *,
        user_id: UUID,
        language_id: UUID,
        num_tasks: int,
    ) -> List[Optional[Task]]:
        """
        Returns a list of tasks for a given language, that have not been audited by the
        user, and that have not been audited 3 times already.
        """
        # don't query at all if we don't have to
        if num_tasks == 0:
            return []

        tasks_query = f"""
        WITH language_tasks AS (
            SELECT
                t.id,
                t.prompt,
                t.completion,
                t.language_id
            FROM task t
            LEFT JOIN task_audit ta
                ON t.id = ta.task_id AND ta.submitted_by = '{user_id}'
            JOIN language_code lc
                ON t.language_id = lc.id
            JOIN dataset ds
                ON t.dataset_id = ds.id
            WHERE ta.task_id IS NULL
                AND lc.id = '{language_id}'
                AND ds.active = TRUE
        ),
        task_audit_counts AS (
            SELECT
                task_id,
                COUNT(*) AS audit_count
            FROM task_audit
            GROUP BY task_id
        )
        SELECT
            id,
            prompt,
            completion,
            language_id
        FROM (
            SELECT
                lt.id,
                lt.prompt,
                lt.completion,
                lt.language_id,
                ROW_NUMBER() OVER (ORDER BY RANDOM()) AS rownum,
                COALESCE(tac.audit_count, 0)
            FROM language_tasks lt
            LEFT JOIN task_audit_counts tac
                ON lt.id = tac.task_id
            WHERE COALESCE(tac.audit_count, 0) < 3
                OR tac.audit_count IS NULL
        ) AS numbered_tasks
        WHERE rownum <= {num_tasks};
        """
        with Session(db.engine) as session:
            tasks = session.query(Task).from_statement(text(tasks_query)).all()

        return tasks

import logging

from datetime import datetime
from uuid import UUID
from typing import Optional

from sqlmodel import Session

from instruct_multilingual import db
from instruct_multilingual.models import (
    TaskAudit,
    TaskAuditReview,
    TaskContributionAudit,
    TaskContributionAuditReview,
)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

class TaskAuditReviewService:

    def create_task_audit_review(
        self,
        *,
        task_audit_id: UUID,
        submitted_by: UUID,
        edited_prompt_rating: int,
        edited_completion_rating: int,
        improved_edited_prompt: Optional[str] = None,
        improved_edited_completion: Optional[str] = None,
        feedback: str,
    ) -> TaskAuditReview:
        """
        Create a task audit review, and then decrement the number of reviews
        that a particular user can receive (the author of the task audit)
        """
        with Session(db.engine) as session:
            review = TaskAuditReview(
                task_audit_id=task_audit_id,
                submitted_by=submitted_by,
                edited_prompt_rating=edited_prompt_rating,
                edited_completion_rating=edited_completion_rating,
                improved_prompt=improved_edited_prompt,
                improved_completion=improved_edited_completion,
                improvement_feedback=feedback,
            )
            session.add(review)
            session.commit()
            session.refresh(review)

        return review


class TaskContributionAuditReviewService:

    def create_task_contribution_audit_review(
        self,
        *,
        task_contribution_audit_id: UUID,
        submitted_by: UUID,
        edited_prompt_rating: int,
        edited_completion_rating: int,
        improved_edited_prompt: Optional[str] = None,
        improved_edited_completion: Optional[str] = None,
        feedback: str,
    ) -> TaskContributionAuditReview:
        """
        Create a task contribution audit review, and then decrement the number of reviews
        that a particular user can receive (the author of the task contribution audit)
        """
        with Session(db.engine) as session:
            review = TaskContributionAuditReview(
                task_contribution_audit_id=task_contribution_audit_id,
                submitted_by=submitted_by,
                edited_prompt_rating=edited_prompt_rating,
                edited_completion_rating=edited_completion_rating,
                improved_prompt=improved_edited_prompt,
                improved_completion=improved_edited_completion,
                improvement_feedback=feedback,
            )
            session.add(review)
            session.commit()
            session.refresh(review)

        return review
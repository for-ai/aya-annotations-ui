import logging
from uuid import UUID

from fastapi import status
from sqlmodel import Session

from instruct_multilingual import db
from instruct_multilingual.exceptions import InstructMultilingualAPIError
from instruct_multilingual.models.task_1_submission import Task1Submission
from instruct_multilingual.models.task_3_submission import Task3Submission
from instruct_multilingual.models.task_contribution import TaskContribution
from instruct_multilingual.schemas.user import UserTaskContributionPaginationResponseSchema

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)


class UserContributionService:

    @staticmethod
    def fetch_task_contributions_by_user(
            task_type: str,
            user_id: UUID,
            page: int = 1,
            page_size: int = 20
    ) -> UserTaskContributionPaginationResponseSchema:
        """ Fetch contributions for a Task type by a specific user with pagination. """

        if task_type == 'task1':
            entity = Task1Submission
        elif task_type == 'task2':
            entity = TaskContribution
        elif task_type == 'task3':
            entity = Task3Submission

        try:
            with Session(db.engine) as session:
                total_count = session.query(entity).filter(entity.submitted_by == user_id).count()
                task_submissions = (session.query(entity)
                                      .filter(entity.submitted_by == user_id)
                                      .order_by(entity.created_at.desc())
                                      .limit(page_size)
                                      .offset((page - 1) * page_size)
                                      .all())

            total_pages = -(-total_count // page_size)
            return UserTaskContributionPaginationResponseSchema(total_count=total_count, page=page, page_size=page_size,
                                                                total_pages=total_pages, results=task_submissions)

        except Exception as e:
            logger.error(e)
            raise InstructMultilingualAPIError(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving the contributions for {task_type}",
            )

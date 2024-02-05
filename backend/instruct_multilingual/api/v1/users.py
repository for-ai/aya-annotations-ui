import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from psycopg2.extras import NumericRange
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session

from instruct_multilingual import db
from instruct_multilingual.exceptions import InstructMultilingualAPIError
from instruct_multilingual.models.country_code import CountryCode
from instruct_multilingual.models.language_code import LanguageCode
from instruct_multilingual.models.user import User
from instruct_multilingual.schemas.user import (
    UserCountryOptionsResponseSchema,
    UserLanguageOptionsResponseSchema,
    UserRequestSchema,
    UserResponseSchema,
    UserTaskContributionPaginationResponseSchema,
)
from instruct_multilingual.services.user_contribution_service import (
    UserContributionService,
)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    name="create_user",
)
def create_user(user_request: UserRequestSchema):
    """
    Creates a new user.
    """
    try:
        with Session(db.engine) as session:
            statement = (
                insert(User)
                .values(
                    username=user_request.username,
                    image_url=user_request.image_url,
                )
                .on_conflict_do_update(
                    index_elements=["discord_id"],
                    set_=dict(
                        email=discord_email,
                        username=discord_username,
                        image_url=image_url,
                    ),
                )
                .returning(User)
            )

            user = session.execute(statement).one()
            session.commit()
    except Exception as e:
        logger.error(e)
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error creating user",
        )

    return user


@router.patch(
    "/{user_id}",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
def update_user(
        user_id: UUID,
        user_request: UserRequestSchema,
):
    """
    Updates a user.
    """
    try:
        with Session(db.engine) as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise InstructMultilingualAPIError(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"user not found",
                )

            user.image_url = user_request.image_url
            user.country_code = user_request.country_code
            user.language_codes = user_request.language_codes

            if user_request.age_range is not None:
                min_age = user_request.age_range[0]
                max_age = user_request.age_range[1]
                user.age_range = NumericRange(min_age, max_age, bounds='[]')
            else:
                user.age_range = None

            user.gender = user_request.gender
            user.dialects = user_request.dialects

            session.add(user)
            session.commit()
            session.refresh(user)
    except InstructMultilingualAPIError as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error updating user",
        )

    return user


@router.get("/{user_id}", response_model=UserResponseSchema)
def get_user(
        *,
        user_id: UUID,
):
    """
    Returns a user.
    """
    try:
        with Session(db.engine) as session:
            user = session.get(User, user_id)
    except Exception as e:
        logger.error(e)
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"an error occurred while retrieving user {user_id}",
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user {user_id} not found",
        )

    return user


@router.get("/options/languages", response_model=UserLanguageOptionsResponseSchema)
def get_language_options():
    """
    Returns a list of language options.
    """
    try:
        with Session(db.engine) as session:
            # sort by name
            languages = session.query(LanguageCode).order_by(LanguageCode.name).all()
    except Exception as e:
        logger.error(e)
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="an error occurred while retrieving language options",
        )

    if languages is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no languages found",
        )

    return UserLanguageOptionsResponseSchema(options=languages)


@router.get("/options/countries", response_model=UserCountryOptionsResponseSchema)
def get_country_options():
    """
    Returns a list of country options.
    """
    try:
        with Session(db.engine) as session:
            countries = session.query(CountryCode).all()
    except Exception as e:
        logger.error(e)
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="an error occurred while retrieving country options",
        )

    if countries is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no countries found",
        )

    return UserCountryOptionsResponseSchema(options=countries)


@router.get(
    "/contributions/{user_id}/{task_type}",
    response_model=UserTaskContributionPaginationResponseSchema,
    status_code=status.HTTP_200_OK
)
def get_contributions(
        *,
        user_id: UUID,
        task_type: str,
        page_number: int = 1,
        page_size: int = 20
):
    """
    Returns the contributions of a user for a specific task.
    """
    try:
        if task_type == "task1" or task_type == "task2" or task_type == "task3":
            return UserContributionService.fetch_task_contributions_by_user(task_type, user_id, page_number, page_size)
        else:
            raise InstructMultilingualAPIError(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid task type {task_type} provided.",
            )

    except Exception as e:
        logger.error(e)
        raise InstructMultilingualAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"an error occurred while retrieving contributions for user {user_id}",
        )

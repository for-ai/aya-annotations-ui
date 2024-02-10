import datetime
import hashlib
import logging
import re
from typing import Optional

import jwt
from aiohttp import ClientSession
from fastapi import HTTPException, APIRouter
from fastapi import Response
from fastapi import status
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session
from sqlmodel import select

from instruct_multilingual import db
from instruct_multilingual.config import get_settings
from instruct_multilingual.exceptions import InstructMultilingualAPIError
from instruct_multilingual.models.user import User
from instruct_multilingual.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

router = APIRouter()
settings = get_settings()

GOOGLE_SCOPES = 'openid email profile'


@router.get("/login")
async def login():
    """
    Redirect to Google OAuth URL.
    """
    oauth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.google_client_id}&redirect_uri={settings.google_redirect_uri}"
        f"&response_type=code&scope={GOOGLE_SCOPES.replace(' ', '%20')}&prompt=consent&access_type=offline"
    )

    return {"url": oauth_url}


async def get_google_access_token(code: str) -> dict:
    """
    Get the access token using the authorization code.
    """
    # Prepare data for the POST request
    data = {
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.google_redirect_uri,
    }

    logger.info('retrieving google access token...')
    # Send a POST request to get the access token
    async with ClientSession() as session:
        async with session.post("https://oauth2.googleapis.com/token", data=data) as response:
            if response.status != 200:
                text = await response.text()
                logger.error(f"error while retrieving access token from google api: {text}")
                raise HTTPException(status_code=response.status, detail="Invalid code")

            logger.info('access token retrieved!')
            return await response.json()


async def get_google_user_info(access_token: str) -> dict:
    """
    Get the user's information using the access token.
    """
    # Prepare the headers for the GET request
    headers = {"Authorization": f"Bearer {access_token}"}

    logger.info(f'making API request to google with access token {access_token}...')

    # Send a GET request to the specified path
    async with ClientSession() as session:
        async with session.get("https://www.googleapis.com/oauth2/v1/userinfo", headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                logger.error(f"error while retrieving user info from google api: {text}")
                raise HTTPException(status_code=response.status, detail="API error")

            logger.info('user info retrieved!')
            return await response.json()


@router.get("/callback")
async def callback(response: Response, code: Optional[str] = None, error: Optional[str] = None,
                   error_description: Optional[str] = None):
    """
    Callback endpoint for Google OAuth.
    """
    if error:
        # Redirect to frontend in case of error
        response.status_code = 302
        response.headers["Location"] = f'{settings.for_ai_url}?message={error_description}'
        return response

    if code:
        try:
            tokens = await get_google_access_token(code)
        except Exception as e:
            # Redirect to frontend in case of another type of error
            response.status_code = 302
            response.headers["Location"] = f'{settings.for_ai_url}?message={str(e)}'
            return response

        access_token, refresh_token = tokens["access_token"], tokens["refresh_token"]

        logger.info(f'access_token: {access_token}')
        logger.info('making API request for user data...')
        user_data = await get_google_user_info(access_token)
        logger.info(f'user data retrieved: {user_data}')

        google_user_id = user_data['id']
        google_picture = user_data['picture']
        google_email = user_data['email']

        # Create a hash using SHA-256 and the google_user_id, then take the first 8 characters
        hash_object = hashlib.sha256(google_user_id.encode())
        random_hash = hash_object.hexdigest()[:8]

        # Combine the name and random hash
        cleaned_name = re.sub(r'\W+', '', user_data["name"])
        derived_username = f'{cleaned_name}_{random_hash}'

        if google_picture is None:
            # Use the default image if the user has no avatar
            image_url = "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y"
        # if the google picture URL is too long then just use the default image as well
        elif len(google_picture) > 1000:
            image_url = "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y"
        else:
            image_url = google_picture

        logger.info('attempting to register user...')
        with Session(db.engine) as session:
            by_email_statement = select(User).where(
                User.email == google_email,
            )
            user_via_email = session.execute(by_email_statement).first()

            if user_via_email is None:
                logger.info(f'user {derived_username} does not exist. registering...')
                try:
                    statement = (
                        insert(User)
                        .values(
                            google_id=google_user_id,
                            username=derived_username,
                            email=google_email,
                            image_url=image_url,
                        )
                        .on_conflict_do_update(
                            index_elements=["google_id"],
                            set_=dict(
                                email=google_email,
                                username=derived_username,
                                image_url=image_url,
                            ),
                        )
                        .returning(User)
                    )

                    user = session.execute(statement).one()
                    session.commit()
                except Exception as e:
                    logger.exception('ran into an issue with registering a user')
                    raise InstructMultilingualAPIError(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"error creating user",
                    )

                logger.info(f'registered user {user} successfully!')

                is_registered = False
            else:
                user = user_via_email[0]
                logger.info(f'user {user} is already registered via email')

                try:
                    logger.info(f'updating google id for user {user}')
                    user.google_id = google_user_id
                    session.commit()
                    session.refresh(user)
                except Exception as e:
                    logger.exception(
                        'ran into an issue with updating google id of an existing user'
                    )
                    raise InstructMultilingualAPIError(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"error updating user email",
                    )
                else:
                    user_schema = UserResponseSchema(**user.__dict__)

                is_registered = True

        exp_time = (datetime.datetime.now(tz=datetime.timezone.utc) +
                    datetime.timedelta(seconds=settings.jwt_expiration_time))

        jwt_access_token = jwt.encode(payload={"sub": access_token, "exp": exp_time}, key=settings.jwt_secret,
                                      algorithm=settings.jwt_algorithm)
        jwt_refresh_token = jwt.encode(payload={"sub": refresh_token, "exp": exp_time}, key=settings.jwt_secret,
                                       algorithm=settings.jwt_algorithm)

        is_complete_profile = False
        if is_registered:
            if user.language_codes is not None and user.language_codes != []:
                is_complete_profile = True

        response.headers["Location"] = (
            f'{settings.for_ai_url}/callback?'
            f'auth_provider=google&'
            f'access_token={jwt_access_token}&'
            f'refresh_token={jwt_refresh_token}&'
            f'user_id={user.id}&'
            f'is_complete_profile={is_complete_profile}'
        )

        response.status_code = 302

        return response

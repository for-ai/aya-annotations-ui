import datetime
import logging
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

DISCORD_SCOPES = 'identify guilds email'

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

router = APIRouter()
settings = get_settings()


async def get_discord_access_token(code: str) -> dict:
    """
    Get the access token using the authorization code.
    """
    # Prepare data for the POST request
    data = {
        "client_id": settings.discord_client_id,
        "client_secret": settings.discord_client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.discord_redirect_uri,
        "scope": DISCORD_SCOPES,
    }

    logger.info('retrieving discord access token...')
    # Send a POST request to get the access token
    async with ClientSession() as session:
        async with session.post(f"{settings.discord_api_base_url}/oauth2/token", data=data) as response:
            if response.status != 200:
                text = await response.text()
                logger.error(f"error while retrieving access token from discord api: {text}")
                raise HTTPException(status_code=response.status, detail="Invalid code")

            logger.info('access token retrieved!')
            return await response.json()


async def get_discord_user_info(access_token: str) -> dict:
    """
    Make an API request to Discord using the access token.
    """
    # Prepare the headers for the GET request
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{settings.discord_api_base_url}/users/@me"

    logger.info(f'making API request to discord url {url} with access token {access_token}...')

    # Send a GET request to the specified path
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                logger.error(f"error while retrieving user info from discord api: {text}")
                raise HTTPException(status_code=response.status, detail="API error")
            return await response.json()


@router.get("/login")
async def login():
    """
    Redirect to Discord OAuth URL.
    """
    oauth_url = (
        f"https://discord.com/oauth2/authorize?client_id={settings.discord_client_id}&redirect_uri={settings.discord_redirect_uri}"
        f"&response_type=code&scope={DISCORD_SCOPES.replace(' ', '%20')}"
    )

    return {"url": oauth_url}


@router.get("/callback")
async def callback(response: Response, code: Optional[str] = None, error: Optional[str] = None,
                   error_description: Optional[str] = None):
    """
    Callback endpoint for Discord OAuth. Register the user if they don't exist.
    """
    if error:
        # Redirect to frontend in case of error
        response.status_code = 302
        response.headers["Location"] = f'{settings.for_ai_url}?message={error_description}'
        return response

    if code:
        try:
            tokens = await get_discord_access_token(code)
        except Exception as e:
            # Redirect to frontend in case of another type of error
            response.status_code = 302
            response.headers["Location"] = f'{settings.for_ai_url}?message={str(e)}'
            return response

        access_token, refresh_token = tokens["access_token"], tokens["refresh_token"]

        logger.info(f'access_token: {access_token}')
        logger.info('making API request for user data...')
        user_data = await get_discord_user_info(access_token)
        logger.info(f'user data retrieved: {user_data}')

        discord_user_id = user_data['id']
        discord_username = user_data['username']
        discord_avatar_id = user_data['avatar']
        discord_email = user_data['email']

        if discord_avatar_id is None:
            # Use the default clyde image if the user has no avatar
            image_url = "https://cdn.discordapp.com/embed/avatars/0.png"
        else:
            image_url = f"https://cdn.discordapp.com/avatars/{discord_user_id}/{discord_avatar_id}.png"

        logger.info('attempting to register user...')
        with Session(db.engine) as session:
            # NOTE: this is not very pretty because we weren't storing
            # discord ids or emails before the username change rollout, so we have
            # to check if the user exists by username or by discord id to account
            # for existing users who may have changed their username even after
            # we've stored their discord id.
            by_email_statement = select(User).where(
                User.email == discord_email,
            )
            by_discord_id_statement = select(User).where(
                User.discord_id == discord_user_id,
            )
            by_username_statement = select(User).where(
                User.username == discord_username,
            )
            user_via_email = session.execute(by_email_statement).first()
            user_via_discord_id = session.execute(by_discord_id_statement).first()
            user_via_username = session.execute(by_username_statement).first()

            if user_via_email is None and user_via_discord_id is None and user_via_username is None:
                logger.info(f'user {discord_username} does not exist. registering...')
                try:
                    statement = (
                        insert(User)
                        .values(
                            discord_id=discord_user_id,
                            username=discord_username,
                            email=discord_email,
                            image_url=image_url,
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
                    logger.exception('ran into an issue with registering a user')
                    raise InstructMultilingualAPIError(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"error creating user",
                    )

                logger.info(f'registered user {user} successfully!')

                is_registered = False
            elif user_via_username is not None:
                # User is already registered via Discord, and we have their username, but we don't
                # have their email or Discord ID.
                # NOTE: due to the discord rollout, and the fact we weren't storing
                # emails / discord ids in the past, we need to update the email and
                # discord id if it's not there for existing users
                user = user_via_username[0]
                logger.info(f'user {user} is already registered via username')
                try:
                    logger.info(f'updating email and discord id for user {user}')
                    user.discord_id = discord_user_id
                    user.email = discord_email
                    session.commit()
                    session.refresh(user)
                except Exception as e:
                    logger.exception(
                        'ran into an issue with updating email and '
                        'discord id of an existing user'
                    )
                    raise InstructMultilingualAPIError(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"error updating user email",
                    )
                else:
                    user_schema = UserResponseSchema(**user.__dict__)

                is_registered = True
            elif user_via_discord_id is not None:
                # User is already registered via Discord, and we have their Discord ID, but we don't
                # have their email or username.
                user = user_via_discord_id[0]
                logger.info(f'user {user} is already registered and has a discord id')

                try:
                    logger.info(f'updating username for user {user}')
                    user.username = discord_username
                    user.email = discord_email
                    session.commit()
                    session.refresh(user)
                except Exception as e:
                    logger.exception(
                        'ran into an issue with updating username of an existing user'
                    )
                    raise InstructMultilingualAPIError(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"error updating user username",
                    )
                else:
                    user_schema = UserResponseSchema(**user.__dict__)

                is_registered = True
            else:
                # User is already registered via Google, and we have their email, but we don't
                # have their discord id or username.
                user = user_via_email[0]
                logger.info(f'user {user} is already registered and has an email')

                try:
                    logger.info(f'updating username for user {user}')
                    user.username = discord_username
                    user.discord_id = discord_user_id
                    session.commit()
                    session.refresh(user)
                except Exception as e:
                    logger.exception(
                        'ran into an issue with updating username of an existing user'
                    )
                    raise InstructMultilingualAPIError(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"error updating user username",
                    )
                else:
                    user_schema = UserResponseSchema(**user.__dict__)

                is_registered = True

        exp_time = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
            seconds=settings.jwt_expiration_time)

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
            f'auth_provider=discord&'
            f'access_token={jwt_access_token}&'
            f'refresh_token={jwt_refresh_token}&'
            f'user_id={user.id}&'
            f'is_complete_profile={is_complete_profile}'
        )

        response.status_code = 302

        return response

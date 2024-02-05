import logging

import jwt
from fastapi import APIRouter
from fastapi import HTTPException, Header, Query
from fastapi import Response

from instruct_multilingual.api.v1.auth_discord import get_discord_user_info
from instruct_multilingual.api.v1.auth_google import get_google_user_info
from instruct_multilingual.config import get_settings

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

router = APIRouter()
settings = get_settings()


@router.get("/authenticated")
async def authenticated(authorization: str = Header(None), auth_provider: str = Query(None)):
    """
    Check if a user is authenticated.
    """
    if authorization is None:
        logger.info('user is not authenticated')
        return {"is_authenticated": False}

    jwt_access_token = authorization[len("Bearer "):]

    logger.info('checking if user is already authenticated...')
    logger.info(f'headers: {authorization}')
    logger.info(f'jwt_access_token: {jwt_access_token}')

    try:
        payload = jwt.decode(jwt=jwt_access_token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        access_token = payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if auth_provider == 'google':
        print("auth_provider is google")
        try:
            await get_google_user_info(access_token)
            authenticated = True
            print("authenticated is true")
        except HTTPException:
            authenticated = False
            print("authenticated is false")
    elif auth_provider == 'discord':
        try:
            await get_discord_user_info(access_token)
            authenticated = True
        except HTTPException:
            authenticated = False
    else:
        authenticated = False
        raise HTTPException(status_code=401, detail="Invalid auth provider")

    logger.info(f'user is authenticated? {authenticated}')
    return {"is_authenticated": authenticated}


@router.get("/logout")
async def logout(response: Response):
    """
    Logout the user.
    """
    # Redirect to frontend
    return {"redirect_url": f'{settings.for_ai_url}'}

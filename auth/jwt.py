"""
Functions for authentication by jwt
"""
from config.setup import settings
from datetime import datetime, timedelta, timezone
from typing import Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.token import TokenData
from typing_extensions import Annotated
from .utils import get_user
from models.users import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login')
"""OAuth2 flow to be used as a dependency for authentication.."""


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
):
    """Creates access token for username in data with expiration time."""
    to_encode = data.copy()

    # set expiration time (if not set in config default 15mins)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    # create a token based on username, secret key & algorithm
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM
    )

    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Verifies given token and finds and returns the user associated."""
    # exception to raise when authorization fails
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        # decode given token using predefined secret key & algorithm
        payload = jwt.decode(
            token, settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM]
        )

        # get user name from decoded payload
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:    # verification failed
        raise credentials_exception

    # get and return user from db based on decoded username
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Checks if current user is disabled and returns it if not disabled."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user

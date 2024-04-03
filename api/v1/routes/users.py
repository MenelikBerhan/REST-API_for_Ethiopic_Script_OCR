"""Image endpoints
"""
from config.setup import settings
from db.mongodb import db_client
from fastapi import APIRouter, Body, Depends, status, HTTPException
from models.token import Token
from models.users import User, UserInCreate, UserInDB, UserInResponse
from auth.jwt import create_access_token, get_current_active_user
from auth.utils import authenticate_user, check_free_username_and_email,\
    get_password_hash
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from datetime import timedelta

# create a router with `/pdf` prefix
users_router = APIRouter(prefix='/user')


@users_router.post(
    '/register',
    response_model=UserInResponse,
    tags=['authentication'],
    status_code=status.HTTP_201_CREATED,
)
async def register(
        user: UserInCreate = Body(...)
):
    """
    Register user
    """
    # check if any user exists with given username & password.
    # if found raises HTTP exception
    await check_free_username_and_email(user.username, user.email)

    # hash given password and store user in db
    user_dict = user.model_dump(exclude=['id'])
    hashed_password = get_password_hash(user.password)
    user_db = UserInDB(**user_dict, hashed_password=hashed_password)

    insert_result = await db_client.db.users.insert_one(
        user_db.model_dump(exclude=['id'])
    )

    # add id created by db to user_dict and return it
    user_dict['id'] = insert_result.inserted_id

    return user_dict


@users_router.post(
    '/login',
    tags=['authentication'],
    response_model=Token
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    Logs in a user based on username & password, by creating and returning
    access token with expiration time.
    """
    # retrieve user from db using given username & password
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    # create token with expiry time and return it
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type='bearer')


@users_router.get(
        '/me/',
        response_model=UserInResponse,
        tags=['authentication']
    )
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Get current user based on token in header.
    """
    return current_user

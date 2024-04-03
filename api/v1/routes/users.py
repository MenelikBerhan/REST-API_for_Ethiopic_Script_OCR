"""Image endpoints
"""
from auth.utils import authenticate_user, check_free_username_and_email,\
    get_password_hash
from auth.jwt import create_access_token, get_current_active_user
from config.setup import settings
from datetime import timedelta
from db.mongodb import db_client
from fastapi import APIRouter, Body, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.token import Token
from models.users import User, UserInCreate, UserInDB, UserInResponse
from typing_extensions import Annotated

# create a router with `/user` prefix
users_router = APIRouter(prefix='/user')


@users_router.post(
    '/register',
    response_model=UserInResponse,
    tags=['authentication'],
    status_code=status.HTTP_201_CREATED,
    response_description='__Created User__'
)
async def register_user(
        user: UserInCreate = Body(...)
):
    """
    ### Register user
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
    response_model=Token,
    response_description='__Access Token__'
)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    ### Logs in a user based on username & password.
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
        tags=['authentication'],
        response_description='__Current User__'
)
async def get_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    ### Get current user.
    """
    return current_user

"""Image endpoints
"""
from db.mongodb import db_client
from fastapi import APIRouter, Body, Depends, status, HTTPException
from models.users import User, UserInCreate, UserInDB, UserInLogin, UserInResponse

from auth.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_password_hash, get_current_active_user, Token
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from datetime import timedelta

# create a router with `/pdf` prefix
users_router = APIRouter(prefix='/users')
    


async def check_free_username_and_email(username, email):
    user = await db_client.db.users.find_one({'username': username})
    if user:
        raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='User with this username already exists',
            )
    
    user = await db_client.db.users.find_one({'email': email})
    if user:
        raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='User with this email already exists',
            )


@users_router.post(
    '/register',
    response_model=UserInResponse,
    tags=["authentication"],
    status_code=status.HTTP_201_CREATED,
)
async def register(
        user: UserInCreate = Body(...)
):
    await check_free_username_and_email(user.username, user.email)

    user_dict = user.model_dump(exclude=['id'])
    hashed_password = get_password_hash(user.password)

    user_db = UserInDB(**user_dict, hashed_password=hashed_password)

    insert_result = await db_client.db.users.insert_one(user_db.model_dump(exclude=['id']))

    user_dict['id'] = insert_result.inserted_id

    return  user_dict



@users_router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@users_router.get("/me/", response_model=UserInResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@users_router.get("/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

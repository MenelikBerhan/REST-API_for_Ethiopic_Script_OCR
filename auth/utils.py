"""
Utility functions for authentication by jwt
"""
from db.mongodb import db_client
from fastapi import HTTPException, status
from passlib.context import CryptContext
from models.users import UserInDB


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
"""Password context for hashing & verifying passwords"""


def verify_password(plain_password, hashed_password):
    """Checks if plain password matches the hashed one."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Runs password through selected algorithm, returning resulting hash."""
    return pwd_context.hash(password)


async def get_user(username: str):
    """Finds & returns user from database based on given username."""
    user = await db_client.db.users.find_one({'username': username})
    if user:
        return UserInDB(**user)


async def authenticate_user(username: str, password: str):
    """Authenticates user based on given username & password."""
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def check_free_username_and_email(username, email):
    """Checks if no user exists for given username and email."""
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

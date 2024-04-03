"""Users model
"""
from models.base_model import APIBaseModel
from pydantic import BaseModel, EmailStr
from typing import Union


class UserInResponse(APIBaseModel):
    """User in reponses for all endpoints."""
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


class User(UserInResponse):
    """User in path operations."""
    disabled: Union[bool, None] = False


class UserInDB(User):
    """User in db with hashed password."""
    hashed_password: str


class UserInLogin(BaseModel):
    """User in request to POST /login."""
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    """User in request to POST /user/register"""
    username: str
    full_name: Union[str, None] = None

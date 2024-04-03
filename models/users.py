"""Users model
"""
from models.base_model import APIBaseModel
from pydantic import BaseModel, EmailStr
from typing import Union


class UserInResponse(APIBaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None

class User(UserInResponse):
    disabled: Union[bool, None] = False

class UserInDB(User):
    hashed_password: str

class UserInLogin(BaseModel):
    email: EmailStr
    password: str

class UserInCreate(UserInLogin):
    username: str
    full_name: Union[str, None] = None

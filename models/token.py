"""
Token model classes
"""
from pydantic import BaseModel
from typing import Union


class Token(BaseModel):
    """Abstraction of Token in response for `POST /login`."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Abstraction of token data in request for protected endpoints."""
    username: Union[str, None] = None

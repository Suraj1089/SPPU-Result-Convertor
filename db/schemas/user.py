from typing import Union

from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: str


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: int
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

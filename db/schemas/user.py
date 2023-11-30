from typing import Union

from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: int
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

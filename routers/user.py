from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.schemas.user import UserInDB, UserCreate, Token
from internal.config import settings
from utils.user import create_user
from utils.user import get_user, create_access_token, authenticate_user, get_current_active_user
from typing import Union
from fastapi import status, Response
from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from db.models.user import User

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/', response_model=Token, status_code=status.HTTP_201_CREATED)
def create(user: UserCreate, db: Session = Depends(get_db)):
    new_user: Union[UserInDB, None] = create_user(db, user)
    print(new_user)
    if not new_user:
        return Response(content=f'User with email {user.email} already exist',
                        status_code=status.HTTP_403_FORBIDDEN)
    token = create_access_token(subject=new_user.id, expires_delta=timedelta(minutes=1))
    return Token(access_token=token, token_type='bearer')


@router.get('/', response_model=Union[UserInDB, None])
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    return get_user(username, db)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserInDB)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

from datetime import timedelta
from typing import Annotated
from typing import Union, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.database import get_db
from db.models.user import User
from db.schemas.user import UserInDB, UserCreate, Token, UserOutDB
from internal.config import settings
from utils.email_utils import send_new_account_email
from utils.user import (
    create_access_token,
    authenticate_user,
    get_current_active_user,
    get_user_by_email
)
from utils.user import create_user, get_user_by_query

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/', response_model=Token, status_code=status.HTTP_201_CREATED)
async def create(user_in: UserCreate, db: Session = Depends(get_db)) -> Token:
    user = get_user_by_email(db, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail=f"The user with {user_in.email} already exists.",
        )
    new_user: Union[UserInDB, None] = create_user(db, user_in)
    if settings.EMAILS_ENABLED:
        # TODO: Use Anyone method either Email or Password  # pylint: disable=fixme
        await send_new_account_email(email_to=new_user.email, subject="New Account creation email",
                                     html_body="New Account creation body")
    token = create_access_token(subject=new_user.email, expires_delta=timedelta(minutes=1))
    return Token(access_token=token, token_type='bearer')


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
        user.email, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserInDB)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@router.get('/{query}', response_model=UserOutDB)
def get_user(query: Optional[str], db: Session = Depends(get_db)):
    user = get_user_by_query(query, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found")
    return user

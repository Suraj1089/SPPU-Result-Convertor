from datetime import datetime, timedelta
from typing import Union, Type, Any, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from db.database import get_db
from db.models.user import User
from db.schemas.user import UserCreate, UserInDB, TokenData
from internal.config import settings
from utils.logging_utils import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_user(db: Session, user: UserCreate) -> Union[UserInDB, None]:
    existing_user = db.query(User).filter(User.email==user.email).first()
    if existing_user:
        logger.error({
            'event_type': 'USER',
            'event_subtype': '',
            'event_name': 'CREATE_USER',
            'new_user': user,
            'error': 'Existing User found',
            'existing_user': existing_user
        })
        return None
    user.password = get_password_hash(user.password)
    user_in_db = User(**user.model_dump())
    db.add(user_in_db)
    db.commit()
    db.refresh(user_in_db)
    return user_in_db


def get_user(username: str, db: Session = Depends(get_db)) -> Union[UserInDB, None]:
    """
    :param username:
    :param db:
    :return:
    """
    user: Union[UserInDB, None] = db.query(User).filter(User.email == username).first()
    if not user:
        return None
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[Type[User]]:
    """
    :param db:
    :param skip:
    :param limit:
    :return:
    """
    return db.query(User).offset(skip).limit(limit).all()


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    :param token:
    :param settings:
    :return:
    """
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    user = get_user(token_data.username)
    if user is None:
        raise credential_exception
    return user


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str) -> [UserInDB, bool]:
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

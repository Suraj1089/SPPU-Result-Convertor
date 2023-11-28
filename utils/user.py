from typing import Union, Type

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from db.database import get_db
from db.models.user import User
from db.schemas.user import UserCreate, UserInDB
from internal.config import Settings, get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_user(db: Session, user: UserCreate) -> UserInDB:
    user_in_db = User(first_name=user.first_name, last_name=user.last_name, email=user.email,
                      password=user.password)
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


def get_current_user(token: str = Depends(oauth2_scheme),
                     settings: Settings = Depends(get_settings)):
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
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHMS])
        username: str = payload.get("sub")
    except JWTError as ex:
        raise credential_exception from ex
    user = get_user(username)
    if user is None:
        raise credential_exception
    return user

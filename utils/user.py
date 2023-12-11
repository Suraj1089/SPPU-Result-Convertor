from datetime import datetime, timedelta
from typing import Optional, Dict
from typing import Union, Type, Any

from jinja2 import Template
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import or_
from sqlalchemy.orm import Session

from db.models.user import User
from db.schemas.user import UserCreate, UserInDB
from internal.config import settings
from utils.logging_utils import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email: str) -> Optional[UserInDB]:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> Union[UserInDB, None]:
    existing_user = db.query(User).filter(User.email == user.email).first()
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


def get_user(username: str, db: Session) -> Union[UserInDB, None]:
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


def get_user_by_query(query: str, db: Session) -> Union[UserInDB, None]:
    user = db.query(User).filter(
        or_(
            User.first_name.ilike(f"%{query}%"),
            User.last_name.ilike(f"%{query}%"),
            User.email.ilike(f"%{query}%")
        )
    ).first()
    return user


def fade_data_in_html(html_template_str: str, data: Dict[str, str]) -> str:
    template = Template(html_template_str)
    rendered_html = template.render(data)
    return rendered_html


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db.schemas.user import UserInDB, UserCreate
from internal.config import get_settings
from utils.user import create_user as user_create
from utils.user import get_user as user_get

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(get_settings), ]
)


@router.post('/', response_model=UserInDB)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_create(db, user)


@router.get('/', response_model=UserInDB)
def get_user(username: str, db: Session = Depends(get_db)):
    return user_get(username, db)

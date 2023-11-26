from fastapi import APIRouter, Depends
from typing import Annotated
from internal.config import get_settings, Settings

router = APIRouter(
    prefix='/files',
    tags=['files'],
    dependencies=[Depends(get_settings), ]
)
from pydantic import BaseModel
class UploadFileSchema(BaseModel):
    file: str

@router.get('/results')
def upload(file: UploadFileSchema, settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "hello": "word",
        "file": file
    }
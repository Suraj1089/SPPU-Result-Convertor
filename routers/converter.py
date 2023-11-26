from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import File, UploadFile

from internal.config import get_settings

router = APIRouter(
    prefix='/files',
    tags=['files'],
    dependencies=[Depends(get_settings), ]
)


@router.post("/uploadFile/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A result file read as UploadFile")]
):
    return {
        "filename": file.filename, "file": file.file, "content_type": file.content_type,
        "size": file.size
    }

@router.get("/uploadFile/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A result file read as UploadFile")]
):
    return {
        "filename": file.filename, "file": file.file, "content_type": file.content_type,
        "size": file.size
    }
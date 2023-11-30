from typing import Annotated

from fastapi import APIRouter
from fastapi import File, UploadFile

router = APIRouter(
    prefix='/files',
    tags=['files']
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
async def file_get(
    file: Annotated[UploadFile, File(description="A result file read as UploadFile")]
):
    return {
        "filename": file.filename, "file": file.file, "content_type": file.content_type,
        "size": file.size
    }

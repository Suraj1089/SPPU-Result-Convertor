from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import File, UploadFile
from api.deps import get_current_active_user


router = APIRouter(
    prefix='/files',
    tags=['files'],
    dependencies=[Depends(get_current_active_user)]
)


@router.post("/uploadFile/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A result file read as UploadFile")]
):
    return {
        "filename": file.filename, "file": file.file, "content_type": file.content_type,
        "size": file.size
    }

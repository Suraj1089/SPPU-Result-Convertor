from pydantic import BaseModel


class UploadFileSchema(BaseModel):
    file: str

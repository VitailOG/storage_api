from datetime import datetime

from pydantic import BaseModel


class FileInfoResponseSchema(BaseModel):
    id: int
    filename: str
    content_type: str
    size: int
    created_at: datetime

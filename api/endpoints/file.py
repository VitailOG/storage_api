from urllib.parse import quote
from typing import Annotated, Any

from psycopg.rows import class_row

from fastapi import APIRouter, UploadFile, Path, Response, Depends

from repositories.file import FileRepository
from api.dependencies.db import get_db_cursor
from api.schemas.file import FileInfoResponseSchema


router = APIRouter(tags=['file'])


@router.get("/top")
async def top_file(
    repo: Annotated[FileRepository, Depends(get_db_cursor(FileRepository, row_factory=class_row(dict)))]
) -> list[FileInfoResponseSchema]:
    return await repo.top()


@router.post("/files/")
async def upload_file(
    file: UploadFile,
    repo: Annotated[FileRepository, Depends(get_db_cursor(FileRepository))]
):
    pk = await repo.upload(file.filename, file.size, file.content_type, await file.read())
    return {"pk": pk}


@router.get("/files/{id}")
async def download_file(
    pk: Annotated[int, Path(..., alias='id')],
    repo: Annotated[FileRepository, Depends(get_db_cursor(FileRepository))]
):
    content, filename = await repo.get_content(pk)
    return Response(
        content=content,
        headers={
            "Content-Disposition": f"attachment;filename={quote(filename)}",
            "Content-Type": "application/octet-stream"
        }
    )


@router.head("/files/{id}")
async def info_file(
    pk: Annotated[int, Path(..., alias='id')],
    repo: Annotated[FileRepository, Depends(get_db_cursor(FileRepository))]
):
    content_type, size, created_at = await repo.get_info_file(pk)
    response = Response()
    response.headers['Content-Type'] = content_type
    response.headers['Content-Length'] = str(size)
    response.headers['X-Created-At'] = created_at.strftime("%Y-%m-%d %H:%M:%S.%f")
    return response

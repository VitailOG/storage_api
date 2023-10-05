from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from exceptions import NotFoundError


async def does_not_error_handler(_: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        {"errors": True, "message": "Object not found"},
        status_code=status.HTTP_404_NOT_FOUND
    )


async def global_error_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        {"errors": True, "message": "Internal Server Error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

import psycopg

from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from exceptions import NotFoundError
from errors import global_error_handler
from errors import does_not_error_handler
from api.endpoints.file import router as file_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    conn = await psycopg.AsyncConnection.connect(settings.db_connection_string, autocommit=True)
    application.state.conn_db = conn

    async with conn.cursor() as cursor:
        with open(settings.BASE_DIR / "sql/table.sql", "r") as file:
            await cursor.execute(file.read())
            await conn.commit()
    yield
    await conn.close()


def get_application() -> FastAPI:
    application = FastAPI(lifespan=lifespan)

    # include routers
    application.include_router(file_router)

    # include errors
    application.add_exception_handler(NotFoundError, does_not_error_handler)
    application.add_exception_handler(Exception, global_error_handler)

    return application


app = get_application()

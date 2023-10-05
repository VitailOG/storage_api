from fastapi import Request


def get_db_cursor(repository, **cursor_args):
    async def _get_db_cursor(request: Request):
        async with request.app.state.conn_db.cursor(**cursor_args) as cursor:
            yield repository(cursor)
    return _get_db_cursor

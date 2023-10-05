from typing import Any

from exceptions import NotFoundError
from repositories import BaseRepository


class FileRepository(BaseRepository):

    async def top(self):
        query_result = await self._executor(
            ("SELECT id, filename, content_type, size, created_at FROM file_info ORDER BY size DESC LIMIT 10",),
            False
        )
        return await query_result.fetchall()

    @staticmethod
    def _get_raw_by_id(columns: list[str]) -> str:
        return "SELECT {} FROM file_info where id=%s".format(", ".join(columns))

    async def _executor(self, params: tuple[Any], detail: bool = True):
        query_result = await self.cursor.execute(*params)

        if detail and query_result.rowcount == 0:
            raise NotFoundError

        return query_result

    async def get_content(self, pk: int):
        query_result = await self._executor((self._get_raw_by_id(["content", "filename"]), (pk,)))
        return await query_result.fetchone()

    async def get_info_file(self, pk: int):
        query_result = await self._executor((self._get_raw_by_id(["content_type", "size", "created_at"]), (pk,)))
        return await query_result.fetchone()

    async def upload(
        self,
        filename: str,
        size: int,
        content_type: str,
        content: bytes
    ):
        raw_query = """
            INSERT INTO file_info (filename, content_type, size, content) VALUES (%s, %s, %s, %s) RETURNING id;
        """
        query_result = await self._executor((raw_query, (filename, content_type, size, content)), False)
        return await query_result.fetchone()

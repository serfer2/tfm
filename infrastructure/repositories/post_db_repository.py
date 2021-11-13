from typing import (
    Any,
    Iterable,
)

from domain.models import (
    Post,
    Thread,
)
from domain.repositories import PostRepository
from infrastructure.db import open_dbc


@PostRepository.register
class PostDBRepository:

    def __init__(self, dbc: Any = None):
        self._dbc = dbc or open_dbc()

    def __del__(self):
        try:
            self._dbc.close()
        except Exception:
            pass

    def read(self, thread: Thread) -> Iterable[Post]:
        posts = []
        rows = self._get_from_db(thread=thread, only_first=False)
        for row in rows:
            posts.append(
                Post(
                    id=int(row[0]),
                    site=thread.site,
                    forum=thread.forum,
                    thread=int(row[1]),
                    content=row[3],
                    timestamp=row[2],
                )
            )
        return posts

    def read_first(self, thread: Thread) -> Post:
        rows = self._get_from_db(thread=thread, only_first=True)
        if not rows:
            return None
        return Post(
            id=int(rows[0][0]),
            site=thread.site,
            forum=thread.forum,
            thread=int(rows[0][1]),
            content=rows[0][3],
            timestamp=rows[0][2],
        )

    def _get_from_db(self, thread: Thread, only_first: bool = True) -> Iterable[Post]:
        cur = self._dbc.cursor()
        query = """
            SELECT
                p."IdPost",
                p."Thread",
                p."Timestamp",
                p."Content"
            FROM
                "Post" p
            WHERE
                "Thread" = %s
            ORDER BY
                p."Timestamp" ASC
        """
        if only_first:
            query += """ LIMIT 1 """
        cur.execute(query, (thread.id, ))
        return cur.fetchall()

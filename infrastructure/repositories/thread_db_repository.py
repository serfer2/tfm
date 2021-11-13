from typing import (
    Any,
    Iterable,
)

from domain.models import (
    Forum,
    Thread,
)
from domain.repositories import ThreadRepository
from infrastructure.db import open_dbc
from shared.constants import (
    CRAWLING_DIRECTION_BACKWARD,
    CRAWLING_DIRECTION_FORWARD,
)


@ThreadRepository.register
class ThreadDBRepository:

    def __init__(self, dbc: Any = None):
        self._dbc = dbc or open_dbc()

    def __del__(self):
        try:
            self._dbc.close()
        except Exception:
            pass

    def read(self, forum: Forum) -> Iterable[Thread]:
        threads = []
        for row in self._get_from_db(forum=forum):
            dir = CRAWLING_DIRECTION_FORWARD if row[5] == 'FORWARD' else CRAWLING_DIRECTION_BACKWARD
            threads.append(
                Thread(
                    id=int(row[0]),
                    site=int(row[1]),
                    forum=int(row[2]),
                    heading=row[3].strip(),
                    url=row[4].strip(),
                    direction=dir,
                )
            )
        return threads

    def _get_from_db(self, forum: Forum) -> Iterable[Thread]:
        cur = self._dbc.cursor()
        query = """
            SELECT
                t."IdThread",
                t."Site",
                t."Forum",
                t."Heading",
                t."URL",
                t."Direction"
            FROM
                "Site" s,
                "Forum" f,
                "Thread" t
            WHERE
                s."IdSite" = %s AND
                f."Site" = s."IdSite" AND
                f."IdForum" = %s AND
                t."Forum" = f."IdForum"
        """
        cur.execute(query, (forum.site, forum.id))
        return cur.fetchall()

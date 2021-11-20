from typing import (
    Any,
    Iterable,
    List,
)

from psycopg2.extensions import AsIs

from domain.models import Thread
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

    def read(self, site_id: int, forum_ids: List[int]) -> Iterable[Thread]:
        threads = []
        for row in self._get_from_db(site_id=site_id, forum_ids=forum_ids):
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

    def _get_from_db(self, site_id: int, forum_ids: List[int]) -> Iterable[Thread]:
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
                f."IdForum" IN %s AND
                t."Forum" = f."IdForum"
        """
        forums = '(' + ','.join([str(id) for id in forum_ids]) + ')'
        cur.execute(query, (site_id, AsIs(forums)))
        return cur.fetchall()

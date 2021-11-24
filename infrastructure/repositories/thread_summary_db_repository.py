from typing import (
    Any,
    Iterable,
    List,
)

from psycopg2.extensions import AsIs

from domain.models import ThreadSummary
from domain.repositories import ThreadSummaryRepository
from infrastructure.db import open_dbc


@ThreadSummaryRepository.register
class ThreadSummaryDBRepository:

    def __init__(self, dbc: Any = None):
        self._should_close_dbc = dbc is None
        self._dbc = dbc or open_dbc()

    def __del__(self):
        try:
            if self._should_close_dbc:
                self._dbc.close()
        except Exception:
            pass

    def read(self, site_id: int, forum_ids: List[int]) -> Iterable[ThreadSummary]:
        threads = []
        for row in self._get_from_db(site_id=site_id, forum_ids=forum_ids):
            threads.append(
                ThreadSummary(
                    site=row[1],
                    thread=row[2],
                    post=row[0],
                    heading=row[5],
                    first_post_content=row[4],
                    tstamp=row[3],
                )
            )
        return threads

    def _get_from_db(self, site_id: int, forum_ids: List[int]) -> Iterable[ThreadSummary]:
        cur = self._dbc.cursor()
        query = """
            SELECT
                p."IdPost",
                p."Site",
                p."Thread",
                p."Timestamp",
                p."Content",
                t."Heading"
            FROM
                "Post" p
                INNER JOIN (
                    SELECT
                        pp."Thread",
                        MIN(pp."Timestamp") AS min_tstamp
                    FROM "Post" pp
                    WHERE pp."Site" = %s
                    GROUP BY pp."Thread"
                ) g
                ON (g."Thread" = p."Thread" AND	g.min_tstamp = p."Timestamp")
                INNER JOIN "Thread" t ON (
                    t."IdThread" = p."Thread" AND
                    t."Site" = p."Site" AND
                    t."Forum" IN %s AND
                    p."Thread" = g."Thread"
                )
            ORDER BY p."Timestamp" ASC, p."IdPost" ASC
        """
        forums = '(' + ','.join([str(id) for id in forum_ids]) + ')'
        cur.execute(query, (site_id, AsIs(forums)))
        return cur.fetchall()

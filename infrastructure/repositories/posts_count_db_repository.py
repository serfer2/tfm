from typing import (
    Any,
    Iterable,
)

from psycopg2.extensions import AsIs

from domain.models import PostsCount
from domain.repositories import PostsCountRepository
from infrastructure.db import open_dbc


@PostsCountRepository.register
class PostsCountDBRepository:

    def __init__(self, dbc: Any = None):
        self._should_close_dbc = dbc is None
        self._dbc = dbc or open_dbc()

    def __del__(self):
        try:
            if self._should_close_dbc:
                self._dbc.close()
        except Exception:
            pass

    def count_by_site_and_threads(
        self,
        site_id: int,
        thread_ids: Iterable[int],
    ) -> Iterable[PostsCount]:
        cur = self._dbc.cursor()
        query = """
            SELECT
                EXTRACT(year FROM "Timestamp") AS yyyy,
                EXTRACT(month FROM "Timestamp") AS mm,
                COUNT(*) AS post_qty
            FROM
                "Post"
            WHERE
                "Site" = %s AND
                "Thread" IN %s
            GROUP BY 1,2
            ORDER BY yyyy, mm
        """
        threads = '(' + ','.join([str(id) for id in thread_ids]) + ')'
        cur.execute(query, (site_id, AsIs(threads)))
        return self._build_output(site_id, cur.fetchall())

    def count_by_site_and_forums(
        self,
        site_id: int,
        forum_ids: Iterable[int],
    ) -> Iterable[PostsCount]:
        cur = self._dbc.cursor()
        query = """
            SELECT
                EXTRACT(year from p."Timestamp") AS yyyy,
                EXTRACT(month from p."Timestamp") AS mm,
                COUNT(*) AS post_qty
            FROM
                "Post" p
                INNER JOIN "Thread" t ON (
                    t."IdThread" = p."Thread" AND
                    t."Site" = p."Site" AND
                    t."Forum" IN %s
                )
            WHERE
                p."Site" = %s
            GROUP BY 1,2
            ORDER BY yyyy, mm
        """
        forums = '(' + ','.join([str(id) for id in forum_ids]) + ')'
        cur.execute(query, (AsIs(forums), site_id))
        return self._build_output(site_id, cur.fetchall())

    def _build_output(self, site_id: int, rows: Iterable[tuple]) -> Iterable[PostsCount]:
        output = list()
        for row in rows:
            output.append(
                PostsCount(
                    site=site_id,
                    year=str(int(row[0])),
                    month=f'{int(row[1]):02d}',
                    posts=row[2],
                )
            )
        return output

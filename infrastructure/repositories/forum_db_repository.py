from typing import (
    Any,
    Iterable,
    List,
)

from domain.models import Forum
from domain.repositories import ForumRepository
from infrastructure.db import open_dbc


@ForumRepository.register
class ForumDBRepository:

    def __init__(self, dbc: Any = None):
        self._should_close_dbc = dbc is None
        self._dbc = dbc or open_dbc()

    def __del__(self):
        try:
            if self._should_close_dbc:
                self._dbc.close()
        except Exception:
            pass

    def filter_by_url_pattern(self, site_id: int, url_patterns: Iterable[str]) -> List[Forum]:
        forums = []
        for url_pattern in url_patterns:
            row = self._get_from_db(site_id=site_id, url_pattern=url_pattern)
            if row:
                forums.append(
                    Forum(
                        id=int(row[0]),
                        site=int(row[1]),
                        title=row[2].strip(),
                        url=row[3].strip(),
                    )
                )
        return forums

    def _get_from_db(self, site_id: int, url_pattern: str) -> Iterable[Forum]:
        cur = self._dbc.cursor()
        query = """
            SELECT
                f."IdForum",
                f."Site",
                f."Title",
                f."URL"
            FROM
                "Site" s,
                "Forum" f
            WHERE
                s."IdSite" = %s AND
                f."Site" = s."IdSite" AND
                f."URL" LIKE %s
            ORDER BY
                f."URL" ASC
        """
        cur.execute(query, (site_id, url_pattern + '%'))
        return cur.fetchone()

from typing import (
    Any,
    Iterable,
)

from domain.models import (
    Forum,
    Site,
)
from domain.repositories import ForumRepository
from infrastructure.db import open_dbc


@ForumRepository.register
class ForumDBRepository:

    def __init__(self, dbc: Any = None):
        self._dbc = dbc or open_dbc()

    def __del__(self):
        try:
            self._dbc.close()
        except Exception:
            pass

    def read(self, site: Site, url_patterns: Iterable[str]) -> Iterable[Forum]:
        forums = []
        for url_pattern in url_patterns:
            row = self._get_from_db(site=site, url_pattern=url_pattern)
            forums.append(
                Forum(
                    id=int(row[0]),
                    site=int(row[1]),
                    title=row[2].strip(),
                    url=row[3].strip(),
                )
            )
        return forums

    def _get_from_db(self, site: Site, url_pattern: str) -> Iterable[Forum]:
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
        cur.execute(query, (site.id, url_pattern + '%'))
        return cur.fetchone()

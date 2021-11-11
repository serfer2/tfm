import os
from typing import (
    Any,
    List,
)

from psycopg2 import connect


class DBClient:

    def __init__(self, host: str = None, db: str = None, user: str = None, pwd: str = None):
        self._host = host or os.getenv('POSTGRES_HOST')
        self._db = db or os.getenv('POSTGRES_DB')
        self._user = user or os.getenv('POSTGRES_USER')
        self._pwd = pwd or os.getenv('POSTGRES_PASSWORD')
        self._dbc = self._connect()

    def __del__(self):
        try:
            self._dbc.close()
        except Exception:
            pass

    def fetchall(self, query: str) -> List:
        cur = self._dbc.cursor()
        cur.execute(query)
        return cur.fetchall()

    def _connect(self) -> Any:
        return connect(
            host=self._host,
            database=self._db,
            user=self._user,
            password=self._pwd
        )

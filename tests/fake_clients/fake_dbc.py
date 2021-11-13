from typing import (
    Iterable,
    List,
    Tuple,
)


class FakeDBC:

    def __init__(self, registries: Tuple[Tuple] = ()):
        self._cursor = FakeCursor(registries)

    def cursor(self):
        return self._cursor


class FakeCursor:

    def __init__(self, registries: Tuple[Tuple]):
        self._registries = registries
        self._reg_index = 0
        self._queries = []

    @property
    def queries(self):
        return self._queries

    def execute(self, query: str, args: Iterable = None) -> None:
        sql_query = query % args
        self._queries.append(sql_query)

    def fetchall(self) -> List[Tuple]:
        response = []
        if self._registries:
            response = self._registries[self._reg_index]
            self._reg_index += 1
        return response

    def fetchone(self):
        return self.fetchall()

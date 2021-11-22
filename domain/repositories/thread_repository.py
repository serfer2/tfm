from abc import (
    ABC,
    abstractclassmethod,
)
from typing import (
    Iterable,
    List,
)

from domain.models import Thread


class ThreadRepository(ABC):

    @abstractclassmethod
    def read(self, site_id: int, forum_ids: List[int]) -> Iterable[Thread]:
        pass

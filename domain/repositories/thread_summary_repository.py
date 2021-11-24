from abc import (
    ABC,
    abstractclassmethod,
)
from typing import (
    Iterable,
    List,
)

from domain.models import ThreadSummary


class ThreadSummaryRepository(ABC):

    @abstractclassmethod
    def read(self, site_id: int, forum_ids: List[int]) -> Iterable[ThreadSummary]:
        pass

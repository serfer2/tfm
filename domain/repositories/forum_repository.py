from abc import (
    ABC,
    abstractclassmethod,
)
from typing import (
    Iterable,
    List,
)

from domain.models import Forum


class ForumRepository(ABC):

    @abstractclassmethod
    def filter_by_url_pattern(self, site_id: int, url_patterns: Iterable[str]) -> List[Forum]:
        pass

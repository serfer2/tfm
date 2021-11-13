from abc import (
    ABC,
    abstractclassmethod,
)
from typing import Iterable

from domain.models import (
    Forum,
    Site,
)


class ForumRepository(ABC):

    @abstractclassmethod
    def read(self, site: Site, url_patterns: Iterable[str]) -> Iterable[Forum]:
        pass

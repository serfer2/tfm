from abc import (
    ABC,
    abstractclassmethod,
)
from typing import Iterable

from domain.models import (
    Forum,
    Thread,
)


class ThreadRepository(ABC):

    @abstractclassmethod
    def read(self, forum: Forum) -> Iterable[Thread]:
        pass

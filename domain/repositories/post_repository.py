from abc import (
    ABC,
    abstractclassmethod,
)
from typing import Iterable

from domain.models import (
    Post,
    Thread,
)


class PostRepository(ABC):

    @abstractclassmethod
    def read(self, thread: Thread) -> Iterable[Post]:
        pass

    @abstractclassmethod
    def read_first(self, thread: Thread) -> Post:
        pass

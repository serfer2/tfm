from abc import (
    ABC,
    abstractclassmethod,
)
from typing import Iterable

from domain.models import PostsCount


class PostsCountRepository(ABC):

    @abstractclassmethod
    def count_by_site_and_threads(
        self,
        site_id: int,
        thread_ids: Iterable[int],
    ) -> Iterable[PostsCount]:
        pass

    @abstractclassmethod
    def count_by_site_and_forums(
        self,
        site_id: int,
        forum_ids: Iterable[int],
    ) -> Iterable[PostsCount]:
        pass

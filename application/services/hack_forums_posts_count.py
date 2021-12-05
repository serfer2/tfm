from typing import (
    Iterable,
    List
)

from domain.models import Forum
from domain.repositories import (
    ForumRepository,
    PostsCountRepository,
)
from shared.constants import (
    HF_MARKET_SUBFORUMS_FID,
    HF_SITE_ID,
)


class HackForumsPostsCount:

    def __init__(
        self,
        forum_repository: ForumRepository,
        posts_count_repository: PostsCountRepository
    ):
        self._forum_repository = forum_repository
        self._posts_count_repository = posts_count_repository

    def count_market_section_posts(self) -> List[dict]:
        """
        Counts total quantity of posts in Hack Forums "Market" section threads.
        Results are grouped by year and month, ordered by date.
        """
        subforum_ids = [subforum.id for subforum in self._get_market_subforums()]
        posts_count = self._posts_count_repository.count_by_site_and_forums(
            site_id=HF_SITE_ID,
            forum_ids=subforum_ids,
        )
        return [pc.as_dict() for pc in posts_count]

    def count_threads_posts(self, thread_ids: Iterable[int]) -> List[dict]:
        """
        Given a list og Thread ids, counts the quantity of posts and returns
        it grouped by year and month.
        """
        posts_count = self._posts_count_repository.count_by_site_and_threads(
            site_id=HF_SITE_ID,
            thread_ids=thread_ids,
        )
        return [pc.as_dict() for pc in posts_count]

    def _get_market_subforums(self) -> List[Forum]:
        website = 'https://hackforums.net/forumdisplay.php'
        url_patterns = [f'{website}?fid={fid}' for fid in HF_MARKET_SUBFORUMS_FID]
        return self._forum_repository.filter_by_url_pattern(
            site_id=HF_SITE_ID,
            url_patterns=url_patterns
        )

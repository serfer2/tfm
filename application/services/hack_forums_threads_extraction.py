from datetime import datetime
from typing import (
    Iterable,
    List,
    TypedDict,
)

from domain.models import (
    Forum,
    Thread,
)
from domain.repositories import (
    ForumRepository,
    PostRepository,
    ThreadRepository,
)
from shared.constants import (
    HF_SITE_ID,
    HF_MARKET_SUBFORUMS_FID,
    RELATED_TERMS,
)


class ThreadData(TypedDict):
    content: str  # Thread heading + first Post content
    tstamp: datetime  # first Post timestamp


class HackForumsThreadsExtraction:

    def __init__(
        self,
        forum_repository: ForumRepository,
        thread_repository: ThreadRepository,
        post_repository: PostRepository,
    ):
        self._forum_repository = forum_repository
        self._thread_repository = thread_repository
        self._post_repository = post_repository

    def extract(self) -> List[ThreadData]:
        subforum_ids = [subforum.id for subforum in self._get_market_subforums()]
        threads = self._read_forums_threads(forum_ids=subforum_ids)
        return self._filter_threads_by_related_terms(threads=threads)

    def _get_market_subforums(self) -> List[Forum]:
        website = 'https://hackforums.net/forumdisplay.php'
        url_patterns = [f'{website}?fid={fid}' for fid in HF_MARKET_SUBFORUMS_FID]
        return self._forum_repository.filter_by_url_pattern(
            site_id=HF_SITE_ID,
            url_patterns=url_patterns
        )

    def _read_forums_threads(self, forum_ids: List[int]) -> List[Thread]:
        return self._thread_repository.read(
            site_id=HF_SITE_ID,
            forum_ids=forum_ids
        )

    def _filter_threads_by_related_terms(self, threads: Iterable[Thread]) -> List[ThreadData]:
        """
        An interesting thread, from HAckForums, should match almost:
         - One or more terms from tech_terms list.
         - One or more terms from trade_terms ()
        """
        tech_terms = [term.lower() for term in RELATED_TERMS.get('tech_terms')]
        trade_terms = []
        for _, values in RELATED_TERMS.get('trade_terms').items():
            trade_terms += [v.lower() for v in values]

        interesting_threads = []

        for thread in threads:

            first_post = self._post_repository.read_first(thread=thread)
            first_post_text = first_post.content if first_post is not None else ''
            content = f'{thread.heading} {first_post_text}'.strip().lower()

            for tech_term in tech_terms:
                match = False
                if tech_term in content:
                    for trade_term in trade_terms:
                        if trade_term in content:
                            match = True
                            break
                    if match:
                        tstamp = first_post.timestamp if first_post is not None else None
                        interesting_threads.append({'content': content, 'tstamp': tstamp})
                        break

        return interesting_threads

from typing import (
    Iterable,
    List
)

from domain.models import (
    Document,
    Forum,
    ThreadSummary,
)
from domain.repositories import (
    ForumRepository,
    ThreadSummaryRepository,
)
from shared.constants import (
    HF_MARKET_SUBFORUMS_FID,
    HF_SITE_ID,
)
from shared.tools import (
    hf_clean_text,
    tokenize,
)


class HackForumsThreadsExtraction:

    def __init__(
        self,
        forum_repository: ForumRepository,
        thread_summary_repository: ThreadSummaryRepository,
    ):
        self._forum_repository = forum_repository
        self._thread_summary_repository = thread_summary_repository

    def extract(
        self,
        related_terms: Iterable[str],
    ) -> List[Document]:
        subforum_ids = [subforum.id for subforum in self._get_market_subforums()]
        thread_summaries = self._thread_summary_repository.read(
            site_id=HF_SITE_ID,
            forum_ids=subforum_ids
        )
        return self._filter_threads_by_related_terms(
            thread_summaries,
            related_terms,
        )

    def _get_market_subforums(self) -> List[Forum]:
        website = 'https://hackforums.net/forumdisplay.php'
        url_patterns = [f'{website}?fid={fid}' for fid in HF_MARKET_SUBFORUMS_FID]
        return self._forum_repository.filter_by_url_pattern(
            site_id=HF_SITE_ID,
            url_patterns=url_patterns
        )

    def _filter_threads_by_related_terms(
        self,
        thread_summaries: Iterable[ThreadSummary],
        related_terms: Iterable[str],
    ) -> List[Document]:
        """
        An interesting thread, almost one or more related terms.
        """
        tech_terms = [term.lower() for term in related_terms]
        documents = []

        for thread_summary in thread_summaries:

            first_post_text = thread_summary.first_post_content or ''
            content = hf_clean_text(f'{thread_summary.heading} {first_post_text}'.strip().lower())
            word_list = tokenize(content)
            clean_content = ' '.join(word_list)
            matching_terms = []

            for tech_term in tech_terms:
                if tech_term in clean_content:
                    matching_terms.append(tech_term)

            if matching_terms:
                documents.append({
                    'site': thread_summary.site,
                    'thread': thread_summary.thread,
                    'post': thread_summary.post,
                    'content': clean_content,
                    'tstamp': thread_summary.tstamp,
                    'matching_terms': matching_terms,
                    'category': '',
                })

        return documents

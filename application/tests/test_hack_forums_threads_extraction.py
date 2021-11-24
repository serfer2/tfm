from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from expects import (
    equal,
    expect,
)

from application.services import HackForumsThreadsExtraction
from domain.models import Forum
from infrastructure.repositories import (
    ForumDBRepository,
    ThreadSummaryDBRepository,
)
from tests.fake_clients import FakeDBC

FAKE_FIDS = {
    '111': 'A subforum',
    '222': 'Another subforum',
    '333': 'Some other subforum',
}


class HackForumsThreadsExtractionTestCase(TestCase):

    def setUp(self) -> None:
        self._ddos_related_terms = (
            '£', '€', '$,' 'botnet', 'btc', 'cryptostresser', 'ddos', 'ecoin', 'ethereum'
        )
        return super().setUp()

    @patch('application.services.hack_forums_threads_extraction.HF_MARKET_SUBFORUMS_FID', FAKE_FIDS)
    def test_it_gets_market_subforums(self):
        fake_dbc = FakeDBC(
            registries=(
                (1, 0, 'Forum 1', 'https://hackforums.net/forumdisplay.php?fid=111&page=3'),
                (2, 0, 'Forum 2', 'https://hackforums.net/forumdisplay.php?fid=222'),
                (3, 0, 'Forum 3', 'https://hackforums.net/forumdisplay.php?fid=333'),
            )
        )
        forum_repo = ForumDBRepository(dbc=fake_dbc)
        thread_repo = ThreadSummaryDBRepository(dbc=fake_dbc)
        expected_subforums = [
            Forum(
                id=1,
                site=0,
                title='Forum 1',
                url='https://hackforums.net/forumdisplay.php?fid=111&page=3',
            ),
            Forum(
                id=2,
                site=0,
                title='Forum 2',
                url='https://hackforums.net/forumdisplay.php?fid=222',
            ),
            Forum(
                id=3,
                site=0,
                title='Forum 3',
                url='https://hackforums.net/forumdisplay.php?fid=333',
            ),
        ]
        service = HackForumsThreadsExtraction(
            forum_repository=forum_repo,
            thread_summary_repository=thread_repo,
        )

        subforums = service._get_market_subforums()

        expect(subforums).to(equal(expected_subforums))

    @patch('application.services.hack_forums_threads_extraction.HF_MARKET_SUBFORUMS_FID', FAKE_FIDS)
    def test_it_gets_threads_from_subforums_related_with_relevant_terms(self):
        tstamp = datetime.now()
        forum1_db_results = (
            111111,
            0,
            'Forum 1',
            'https://hackforums.net/forumdisplay.php?fid=111&page=3',
        )
        forum2_db_results = (
            222222,
            0,
            'Forum 2',
            'https://hackforums.net/forumdisplay.php?fid=222',
        )
        forum3_db_results = (
            333333,
            0,
            'Forum 3',
            'https://hackforums.net/forumdisplay.php?fid=333',
        )
        thread_summary_db_data_1 = (
            1,
            0,
            3,
            tstamp,
            'from 25$, trusted results! ',
            'Stresser SERVICE',
        )
        thread_summary_db_data_2 = (
            2,
            0,
            4,
            tstamp,
            'just for educational purposes',
            'How to build a DDOS network',
        )
        thread_summaries_query_result = [
            thread_summary_db_data_1,
            thread_summary_db_data_2,
        ]
        fake_dbc = FakeDBC(
            registries=(
                forum1_db_results,
                forum2_db_results,
                forum3_db_results,
                thread_summaries_query_result,
            )
        )
        forum_repo = ForumDBRepository(dbc=fake_dbc)
        thread_repo = ThreadSummaryDBRepository(dbc=fake_dbc)
        service = HackForumsThreadsExtraction(
            forum_repository=forum_repo,
            thread_summary_repository=thread_repo,
        )
        related_terms = ('stresser', 'mirai',)

        interesting_threads_data = service.extract(related_terms=related_terms)

        expect(interesting_threads_data).to(equal([
            {
                'content': 'stresser service from 25$, trusted results!',
                'tstamp': tstamp,
                'matching_terms': ['stresser', ],
                'word_list': ['stresser', 'service', 'from', '25$', 'trusted', 'results'],
            },
        ]))

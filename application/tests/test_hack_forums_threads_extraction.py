from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from expects import (
    equal,
    expect,
)

from application.services import HackForumsThreadsExtraction
from domain.models import (
    Forum,
    Thread,
)
from infrastructure.repositories import (
    ForumDBRepository,
    PostDBRepository,
    ThreadDBRepository,
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
        post_repo = PostDBRepository(dbc=fake_dbc)
        thread_repo = ThreadDBRepository(dbc=fake_dbc)
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
            thread_repository=thread_repo,
            post_repository=post_repo,
        )

        subforums = service._get_market_subforums()

        expect(subforums).to(equal(expected_subforums))

    @patch('application.services.hack_forums_threads_extraction.HF_MARKET_SUBFORUMS_FID', FAKE_FIDS)
    def test_it_gets_threads_from_subforums_related_with_relevant_terms(self):
        tstamp = datetime.now()
        forum1_db_results = (111111, 0, 'Forum 1', 'https://hackforums.net/forumdisplay.php?fid=111&page=3')
        forum2_db_results = (222222, 0, 'Forum 2', 'https://hackforums.net/forumdisplay.php?fid=222')
        forum3_db_results = (333333, 0, 'Forum 3', 'https://hackforums.net/forumdisplay.php?fid=333')
        thread1_db_data = (
            111,
            0,
            111111,
            'Stresser SERVICE',
            'https://hackforums.net/showthread.php?tid=5880980',
            'BACKWARD',
        )
        thread2_db_data = (
            222,
            0,
            222222,
            'How to build a DDOS network',
            'https://hackforums.net/showthread.php?tid=5882071',
            'BACKWARD',
        )
        thread3_db_data = (
            333,
            0,
            333333,
            'Ganchillo course',
            'https://hackforums.net/showthread.php?tid=5882071',
            'BACKWARD',
        )
        threads_query_result = [thread1_db_data, thread2_db_data, thread3_db_data]
        thread_1_posts_db_query_results = [(1, 111, tstamp, 'from 25$, trusted results!'), ]
        thread_2_posts_db_query_results = [(2, 222, tstamp, 'just for educational purposes'), ]
        thread_3_posts_db_query_results = [(3, 333, tstamp, 'For sale, PayPal accepted.'), ]
        fake_dbc = FakeDBC(
            registries=(
                forum1_db_results,
                forum2_db_results,
                forum3_db_results,
                threads_query_result,
                thread_1_posts_db_query_results,
                thread_2_posts_db_query_results,
                thread_3_posts_db_query_results,
            )
        )
        forum_repo = ForumDBRepository(dbc=fake_dbc)
        post_repo = PostDBRepository(dbc=fake_dbc)
        thread_repo = ThreadDBRepository(dbc=fake_dbc)
        positive_match_thread = Thread(
            id=111,
            site=0,
            forum=111111,
            heading='Stresser SERVICE',
            url='https://hackforums.net/showthread.php?tid=5880980',
            direction='BACKWARD',
        )
        service = HackForumsThreadsExtraction(
            forum_repository=forum_repo,
            thread_repository=thread_repo,
            post_repository=post_repo,
        )

        threads = service.extract()

        expect(threads).to(equal([positive_match_thread, ]))

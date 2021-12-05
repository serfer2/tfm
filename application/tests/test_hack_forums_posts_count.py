from unittest import TestCase
from unittest.mock import patch

from expects import (
    equal,
    expect,
)

from application.services import HackForumsPostsCount
from domain.models import Forum
from infrastructure.repositories import (
    ForumDBRepository,
    PostsCountDBRepository,
)
from tests.fake_clients import FakeDBC

FAKE_FIDS = {
    '111': 'A subforum',
    '222': 'Another subforum',
    '333': 'Some other subforum',
}


class HackForumsPostsCountTestCase(TestCase):

    @patch('application.services.hack_forums_posts_count.HF_MARKET_SUBFORUMS_FID', FAKE_FIDS)
    def test_it_gets_market_subforums(self):
        fake_dbc = FakeDBC(
            registries=(
                (1, 0, 'Forum 1', 'https://hackforums.net/forumdisplay.php?fid=111&page=3'),
                (2, 0, 'Forum 2', 'https://hackforums.net/forumdisplay.php?fid=222'),
                (3, 0, 'Forum 3', 'https://hackforums.net/forumdisplay.php?fid=333'),
            )
        )
        forum_repo = ForumDBRepository(dbc=fake_dbc)
        posts_count_repository = PostsCountDBRepository(dbc=fake_dbc)
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
        service = HackForumsPostsCount(
            forum_repository=forum_repo,
            posts_count_repository=posts_count_repository,
        )

        subforums = service._get_market_subforums()

        expect(subforums).to(equal(expected_subforums))

    @patch('application.services.hack_forums_posts_count.HF_MARKET_SUBFORUMS_FID', FAKE_FIDS)
    def test_it_counts_market_section_posts(self):
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
        posts_count_db_data_1 = ('2021', '10', 101)
        posts_count_db_data_2 = ('2021', '11', 123)
        posts_count_query_result = [
            posts_count_db_data_1,
            posts_count_db_data_2,
        ]
        fake_dbc = FakeDBC(
            registries=(
                forum1_db_results,
                forum2_db_results,
                forum3_db_results,
                posts_count_query_result,
            )
        )
        forum_repo = ForumDBRepository(dbc=fake_dbc)
        posts_count_repo = PostsCountDBRepository(dbc=fake_dbc)
        service = HackForumsPostsCount(
            forum_repository=forum_repo,
            posts_count_repository=posts_count_repo,
        )

        market_section_posts_count = service.count_market_section_posts()

        expect(market_section_posts_count).to(equal([
            {
                'site': 0,
                'year': '2021',
                'month': '10',
                'posts': 101,
            }, {
                'site': 0,
                'year': '2021',
                'month': '11',
                'posts': 123,
            },
        ]))

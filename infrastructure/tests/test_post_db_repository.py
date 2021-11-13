from datetime import datetime
from unittest import TestCase

from expects import (
    equal,
    expect,
)

from domain.models import (
    Post,
    Thread,
)
from infrastructure.repositories import PostDBRepository
from shared.constants import CRAWLING_DIRECTION_FORWARD
from tests.fake_clients import FakeDBC


class PostDBRepositoryTestCase(TestCase):

    def test_it_reads_all_thread_posts(self):
        thread_id = 5880532
        forum_id = 999
        post1_timestamp = datetime(2018, 1, 19, 20, 21, 22)
        post2_timestamp = datetime(2020, 2, 20, 21, 22, 23)
        db_registries = (
            [
                (111, thread_id, post1_timestamp, 'Any content'),
                (222, thread_id, post2_timestamp, 'Any other content'),
            ],
        )
        fake_dbc = FakeDBC(registries=db_registries)
        repository = PostDBRepository(dbc=fake_dbc)
        thread = Thread(
            id=thread_id,
            site=0,
            forum=forum_id,
            heading='Any Thread',
            url='https://www.any-url.com',
            direction=CRAWLING_DIRECTION_FORWARD,
        )
        expected_posts = [
            Post(
                id=111,
                site=0,
                forum=forum_id,
                thread=thread_id,
                content='Any content',
                timestamp=post1_timestamp,
            ),
            Post(
                id=222,
                site=0,
                forum=forum_id,
                thread=thread_id,
                content='Any other content',
                timestamp=post2_timestamp,
            ),
        ]

        posts = repository.read(thread=thread)

        expect(posts).to(equal(expected_posts))

    def test_it_reads_first_thread_post(self):
        thread_id = 5880532
        forum_id = 999
        post_timestamp = datetime(2018, 1, 19, 20, 21, 22)
        db_registries = (
            [
                (111, thread_id, post_timestamp, 'Any content'),
            ],
        )
        fake_dbc = FakeDBC(registries=db_registries)
        repository = PostDBRepository(dbc=fake_dbc)
        thread = Thread(
            id=thread_id,
            site=0,
            forum=forum_id,
            heading='Any Thread',
            url='https://www.any-url.com',
            direction=CRAWLING_DIRECTION_FORWARD,
        )
        expected_post = Post(
            id=111,
            site=0,
            forum=forum_id,
            thread=thread_id,
            content='Any content',
            timestamp=post_timestamp,
        )

        posts = repository.read_first(thread=thread)

        expect(posts).to(equal(expected_post))

    def test_it_executes_correct_sql_query_when_reading_first_post(self):
        thread_id = 5880532
        forum_id = 999
        post1_timestamp = datetime(2018, 1, 19, 20, 21, 22)
        db_registries = (
            [
                (111, thread_id, post1_timestamp, 'Any content'),
            ],
        )
        fake_dbc = FakeDBC(registries=db_registries)
        repository = PostDBRepository(dbc=fake_dbc)
        thread = Thread(
            id=thread_id,
            site=0,
            forum=forum_id,
            heading='Any Thread',
            url='https://www.any-url.com',
            direction=CRAWLING_DIRECTION_FORWARD,
        )
        expected_query = """
            SELECT
                p."IdPost",
                p."Thread",
                p."Timestamp",
                p."Content"
            FROM
                "Post" p
            WHERE
                "Thread" = 5880532
            ORDER BY
                p."Timestamp" ASC
            LIMIT 1
        """

        repository.read_first(thread=thread)

        queries = fake_dbc.cursor().queries
        expect(len(queries)).to(equal(1))
        expect(queries[0].replace(' ', '').replace('\n', '')).to(equal(
            expected_query.replace(' ', '').replace('\n', '')
        ))

    def test_it_executes_correct_sql_query_when_reading_all_posts(self):
        thread_id = 5880532
        forum_id = 999
        post1_timestamp = datetime(2018, 1, 19, 20, 21, 22)
        post2_timestamp = datetime(2020, 2, 20, 21, 22, 23)
        db_registries = (
            [
                (111, thread_id, post1_timestamp, 'Any content'),
                (222, thread_id, post2_timestamp, 'Any other content'),
            ],
        )
        fake_dbc = FakeDBC(registries=db_registries)
        repository = PostDBRepository(dbc=fake_dbc)
        thread = Thread(
            id=thread_id,
            site=0,
            forum=forum_id,
            heading='Any Thread',
            url='https://www.any-url.com',
            direction=CRAWLING_DIRECTION_FORWARD,
        )
        expected_query = """
            SELECT
                p."IdPost",
                p."Thread",
                p."Timestamp",
                p."Content"
            FROM
                "Post" p
            WHERE
                "Thread" = 5880532
            ORDER BY
                p."Timestamp" ASC
        """

        repository.read(thread=thread)

        queries = fake_dbc.cursor().queries
        expect(len(queries)).to(equal(1))
        expect(queries[0].replace(' ', '').replace('\n', '')).to(equal(
            expected_query.replace(' ', '').replace('\n', '')
        ))

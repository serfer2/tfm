from unittest import TestCase

from expects import (
    equal,
    expect,
)

from domain.models import PostsCount
from infrastructure.repositories import PostsCountDBRepository
from tests.fake_clients import FakeDBC


class ThreadSummaryDBRepositoryTestCase(TestCase):

    def test_it_counts_posts_by_site_and_threads(self):
        db_registries = (
            [
                (2021, 9, 101),
                (2021, 10, 123),
            ],
        )
        fake_dbc = FakeDBC(registries=db_registries)
        repository = PostsCountDBRepository(dbc=fake_dbc)
        expected_posts_count = [
            PostsCount(
                site=0,
                year='2021',
                month='09',
                posts=101,
            ),
            PostsCount(
                site=0,
                year='2021',
                month='10',
                posts=123,
            ),
        ]

        threads = repository.count_by_site_and_threads(site_id=0, thread_ids=[666, ])

        expect(threads).to(equal(expected_posts_count))

    def test_it_counts_posts_by_site_and_forums(self):
        db_registries = (
            [
                (2021, 9, 101),
                (2021, 10, 123),
            ],
        )
        fake_dbc = FakeDBC(registries=db_registries)
        repository = PostsCountDBRepository(dbc=fake_dbc)
        expected_posts_count = [
            PostsCount(
                site=0,
                year='2021',
                month='09',
                posts=101,
            ),
            PostsCount(
                site=0,
                year='2021',
                month='10',
                posts=123,
            ),
        ]

        threads = repository.count_by_site_and_forums(site_id=0, forum_ids=[666, ])

        expect(threads).to(equal(expected_posts_count))

    def test_it_executes_correct_sql_query_when_counting_posts_by_site_and_threads(self):
        fake_dbc = FakeDBC()
        repository = PostsCountDBRepository(dbc=fake_dbc)
        thread_ids = [999, 666]
        expected_query = """
            SELECT
                EXTRACT(year FROM "Timestamp") AS yyyy,
                EXTRACT(month FROM "Timestamp") AS mm,
                COUNT(*) AS post_qty
            FROM
                "Post"
            WHERE
                "Site" = 0 AND
                "Thread" IN (999, 666)
            GROUP BY 1,2
            ORDER BY yyyy, mm
        """

        repository.count_by_site_and_threads(site_id=0, thread_ids=thread_ids)

        queries = fake_dbc.cursor().queries
        expect(len(queries)).to(equal(1))
        expect(queries[0].replace(' ', '').replace('\n', '')).to(equal(
            expected_query.replace(' ', '').replace('\n', '')
        ))

    def test_it_executes_correct_sql_query_when_counting_posts_by_site_and_forums(self):
        fake_dbc = FakeDBC()
        repository = PostsCountDBRepository(dbc=fake_dbc)
        forum_ids = [999, 666]
        expected_query = """
            SELECT
                EXTRACT(year from p."Timestamp") AS yyyy,
                EXTRACT(month from p."Timestamp") AS mm,
                COUNT(*) AS post_qty
            FROM
                "Post" p
                INNER JOIN "Thread" t ON (
                    t."IdThread" = p."Thread" AND
                    t."Site" = p."Site" AND
                    t."Forum" IN (999, 666)
                )
            WHERE
                p."Site" = 0
            GROUP BY 1,2
            ORDER BY yyyy, mm
        """

        repository.count_by_site_and_forums(site_id=0, forum_ids=forum_ids)

        queries = fake_dbc.cursor().queries
        expect(len(queries)).to(equal(1))
        expect(queries[0].replace(' ', '').replace('\n', '')).to(equal(
            expected_query.replace(' ', '').replace('\n', '')
        ))

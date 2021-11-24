from datetime import datetime
from unittest import TestCase

from expects import (
    equal,
    expect,
)

from domain.models import ThreadSummary
from infrastructure.repositories import ThreadSummaryDBRepository
from tests.fake_clients import FakeDBC


class ThreadSummaryDBRepositoryTestCase(TestCase):

    def test_it_reads_threads_by_sql_querying(self):
        tstamp = datetime.now()
        db_registries = (
            [
                (1, 2, 3, tstamp, 'Some content', 'a heading'),
            ],
        )
        fake_dbc = FakeDBC(registries=db_registries)
        repository = ThreadSummaryDBRepository(dbc=fake_dbc)
        expected_threads = [
            ThreadSummary(
                post=1,
                site=2,
                thread=3,
                tstamp=tstamp,
                first_post_content='Some content',
                heading='a heading',
            ),
        ]

        threads = repository.read(site_id=0, forum_ids=[666, ])

        expect(threads).to(equal(expected_threads))

    def test_it_executes_correct_sql_query(self):
        fake_dbc = FakeDBC()
        repository = ThreadSummaryDBRepository(dbc=fake_dbc)
        forum_ids = [999, 666]
        expected_query = """
            SELECT
                p."IdPost",
                p."Site",
                p."Thread",
                p."Timestamp",
                p."Content",
                t."Heading"
            FROM
                "Post" p
                INNER JOIN (
                    SELECT
                        pp."Thread",
                        MIN(pp."Timestamp") AS min_tstamp
                    FROM "Post" pp
                    WHERE pp."Site" = 0
                    GROUP BY pp."Thread"
                ) g
                ON (g."Thread" = p."Thread" AND	g.min_tstamp = p."Timestamp")
                INNER JOIN "Thread" t ON (
                    t."IdThread" = p."Thread" AND
                    t."Site" = p."Site" AND
                    t."Forum" IN (999,666) AND
                    p."Thread" = g."Thread"
                )
            ORDER BY p."Timestamp" ASC, p."IdPost" ASC
        """

        repository.read(site_id=0, forum_ids=forum_ids)

        queries = fake_dbc.cursor().queries
        expect(len(queries)).to(equal(1))
        expect(queries[0].replace(' ', '').replace('\n', '')).to(equal(
            expected_query.replace(' ', '').replace('\n', '')
        ))

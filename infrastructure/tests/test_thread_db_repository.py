from unittest import TestCase

from expects import (
    equal,
    expect,
)

from domain.models import Thread
from infrastructure.repositories import ThreadDBRepository
from shared.constants import CRAWLING_DIRECTION_BACKWARD
from tests.fake_clients import FakeDBC


class ThreadDBRepositoryTestCase(TestCase):

    def test_it_reads_threads_by_sql_querying(self):
        db_registries = (
            [
                (333, 0, 666, 'I told you!', 'https://music.youtube.com/watch?v=tsJd04bsHwM&list=RDAMVMtsJd04bsHwM', 'BACKWARD'),  # noqa: E501
            ],
        )
        fake_dbc = FakeDBC(registries=db_registries)
        repository = ThreadDBRepository(dbc=fake_dbc)
        forum_id = 666
        expected_threads = [
            Thread(
                id=333,
                site=0,
                forum=forum_id,
                heading='I told you!',
                url='https://music.youtube.com/watch?v=tsJd04bsHwM&list=RDAMVMtsJd04bsHwM',
                direction=CRAWLING_DIRECTION_BACKWARD,
            ),
        ]

        threads = repository.read(site_id=0, forum_ids=[forum_id, ])

        expect(threads).to(equal(expected_threads))

    def test_it_executes_correct_sql_query(self):
        fake_dbc = FakeDBC()
        repository = ThreadDBRepository(dbc=fake_dbc)
        forum_ids = [999, 666]
        expected_query = """
            SELECT
                t."IdThread",
                t."Site",
                t."Forum",
                t."Heading",
                t."URL",
                t."Direction"
            FROM
                "Site" s,
                "Forum" f,
                "Thread" t
            WHERE
                s."IdSite" = 0 AND
                f."Site" = s."IdSite" AND
                f."IdForum" IN (999,666) AND
                t."Forum" = f."IdForum"
        """

        repository.read(site_id=0, forum_ids=forum_ids)

        queries = fake_dbc.cursor().queries
        expect(len(queries)).to(equal(1))
        expect(queries[0].replace(' ', '').replace('\n', '')).to(equal(
            expected_query.replace(' ', '').replace('\n', '')
        ))

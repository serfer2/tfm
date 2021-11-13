from unittest import TestCase

from expects import (
    equal,
    expect,
)

from domain.models import (
    Forum,
    Site,
)
from infrastructure.repositories import ForumDBRepository
from tests.fake_clients import FakeDBC


class ForumDBRepositoryTestCase(TestCase):

    def test_it_reads_forums_by_sql_querying(self):
        db_registries = (
            (123, 0, 'Any title', 'https://www.youtube.com/watch?v=TQrSEsVy35Q&list=RDTQrSEsVy35Q&index=1'),
        )
        fake_dbc = FakeDBC(registries=db_registries)
        repository = ForumDBRepository(dbc=fake_dbc)
        site = Site(
            id=0,
            url='http://www.any_url.com',
            name='A Site',
        )
        expected_forums = [
            Forum(
                id=123,
                site=0,
                title='Any title',
                url='https://www.youtube.com/watch?v=TQrSEsVy35Q&list=RDTQrSEsVy35Q&index=1',
            ),
        ]
        url_patterns = [
            'https://www.youtube.com/watch?v=TQrSEsVy35Q',
        ]

        forums = repository.read(site=site, url_patterns=url_patterns)

        expect(forums).to(equal(expected_forums))

    def test_it_executes_correct_sql_query(self):
        db_registries = (
            (123, 0, 'Any title', 'https://www.youtube.com/watch?v=TQrSEsVy35Q&list=RDTQrSEsVy35Q&index=1'),
        )
        fake_dbc = FakeDBC(registries=db_registries)
        repository = ForumDBRepository(dbc=fake_dbc)
        site = Site(
            id=0,
            url='http://www.any_url.com',
            name='A Site',
        )
        url_patterns = [
            'https://www.youtube.com/watch?v=TQrSEsVy35Q',
        ]
        expected_query = """
            SELECT
                f."IdForum",
                f."Site",
                f."Title",
                f."URL"
            FROM
                "Site" s,
                "Forum" f
            WHERE
                s."IdSite" = 0 AND
                f."Site" = s."IdSite" AND
                f."URL" LIKE https://www.youtube.com/watch?v=TQrSEsVy35Q%
            ORDER BY
                f."URL" ASC
        """

        repository.read(site=site, url_patterns=url_patterns)

        queries = fake_dbc.cursor().queries
        expect(len(queries)).to(equal(1))
        expect(queries[0].replace(' ', '').replace('\n', '')).to(equal(
            expected_query.replace(' ', '').replace('\n', '')
        ))

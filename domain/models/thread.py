from dataclasses import dataclass

from shared.constants import CRAWLING_DIRECTION_FORWARD


@dataclass
class Thread:

    id: int
    site: int
    forum: int
    heading: str
    url: str
    direction: str = CRAWLING_DIRECTION_FORWARD

    def __str__(self) -> str:
        return (
            f'Thread[{self.site}][{self.forum}][{self.id}] - '
            f'{self.heading} ({self.url})'
        )

    def __eq__(self, obj: object) -> bool:
        return (
            self.id == obj.id and
            self.site == obj.site and
            self.forum == obj.forum and
            self.url == obj.url
        )

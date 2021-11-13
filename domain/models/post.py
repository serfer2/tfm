from datetime import datetime

from dataclasses import dataclass


@dataclass
class Post:

    id: int
    site: int
    forum: int
    thread: int
    content: str
    timestamp: datetime

    def __str__(self) -> str:
        return (
            f'Post[{self.site}][{self.forum}][{self.thread}][{self.id}] - '
            f'{self.timestamp} ({self.content})'
        )

    def __eq__(self, obj: object) -> bool:
        return (
            self.id == obj.id and
            self.site == obj.site and
            self.forum == obj.forum and
            self.thread == obj.thread
        )

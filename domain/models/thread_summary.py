from datetime import datetime

from dataclasses import dataclass


@dataclass
class ThreadSummary:

    site: int
    thread: int
    post: int
    heading: str
    first_post_content: str
    tstamp: datetime

    def __str__(self) -> str:
        return (
            f'ThreadSummary[{self.site}][{self.thread}][{self.post}]'
            f'[{self.tstamp}] - {self.heading}'
        )

    def __eq__(self, obj: object) -> bool:
        return (
            self.site == obj.site and
            self.thread == obj.thread and
            self.post == obj.post
        )

from dataclasses import dataclass


@dataclass
class PostsCount:

    site: int
    year: str  # yyyy
    month: str  # mm
    posts: int

    def __str__(self) -> str:
        return f'[{self.site}] {self.year}-{self.month} -> {self.posts}'

    def as_dict(self):
        return {
            'site': self.site,
            'year': self.year,
            'month': self.month,
            'posts': self.posts,
        }

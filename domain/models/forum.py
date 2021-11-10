from dataclasses import dataclass


@dataclass
class Forum:

    id: int
    site: int
    title: str
    url: str

    def __str__(self) -> str:
        return f'Forum[{self.site}][{self.id}] - {self.title} ({self.url})'

    def __eq__(self, obj: object) -> bool:
        return self.id == obj.id and self.site == obj.site and self.url == obj.url

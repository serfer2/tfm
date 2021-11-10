from dataclasses import dataclass


@dataclass
class Site:

    id: int
    url: str
    name: str

    def __str__(self) -> str:
        return f'Site[{self.id}] - {self.name} ({self.url})'

    def __eq__(self, obj: object) -> bool:
        return self.id == obj.id and self.url == obj.url

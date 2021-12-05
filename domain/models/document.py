from datetime import datetime
from typing import (
    List,
    TypedDict,
)


class Document(TypedDict):
    site: int
    thread: int
    post: int
    content: str
    tstamp: datetime
    matching_terms: List[str]
    category: str

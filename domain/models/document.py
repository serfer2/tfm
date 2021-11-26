from datetime import datetime
from typing import (
    List,
    TypedDict,
)


class Document(TypedDict):
    content: str
    tstamp: datetime
    matching_terms: List[str]
    category: str

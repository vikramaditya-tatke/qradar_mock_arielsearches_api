from pydantic import BaseModel, Field
from typing import List, Optional


class Event(BaseModel):
    sourceip: str
    destinationip: Optional[str]
    username: Optional[str]
    logsourceid: int
    categoryname: str
    eventcount: int
    starttime: int = Field(..., description="Event start time in milliseconds since epoch")


class SearchResults(BaseModel):
    events: List[Event]


class SearchRequest(BaseModel):
    query_expression: str


class SearchResponse(BaseModel):
    cursor_id: str
    record_count: int


class SearchStatus(BaseModel):
    completed: bool
    cursor_id: str

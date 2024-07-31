from fastapi import APIRouter, HTTPException
from uuid import uuid4

from app.models import SearchRequest, SearchResponse, SearchResults, SearchStatus

router = APIRouter()

# Load mock data (ideally, move this to a separate module or function later)
with open("app/data/mock_events.json", "r") as f:
    mock_events = SearchResults.parse_raw(f.read()).events

search_store = {}


@router.post("/api/ariel/searches", response_model=SearchResponse, status_code=201)
def create_search(search_request: SearchRequest):
    search_id = str(uuid4())
    # Filter mock_events based on query_expression (replace with your actual filtering logic)
    filtered_events = filter_events(mock_events, search_request.query_expression)

    search_store[search_id] = filtered_events
    return SearchResponse(cursor_id=search_id, record_count=len(filtered_events))


def filter_events(events: list, query_expression: str) -> list:
    # Placeholder function for filtering events (implement your search logic here)
    # For now, we'll just return the events without filtering
    return events


@router.get("/api/ariel/searches/{search_id}", response_model=SearchStatus, status_code=200)
def get_search(search_id: str):
    if search_id not in search_store:
        raise HTTPException(status_code=404, detail="Search not found")
    return SearchStatus(completed=True,cursor_id=search_id)


@router.get("/api/ariel/searches/{search_id}/results", response_model=SearchResults)
def get_search_results(search_id: str):
    if search_id not in search_store:
        raise HTTPException(status_code=404, detail="Search not found")
    return SearchResults(events=search_store[search_id])

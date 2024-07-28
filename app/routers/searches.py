from fastapi import APIRouter, HTTPException
from uuid import uuid4

from app.models import SearchRequest, SearchResponse, SearchResults

router = APIRouter()

# Load mock data (ideally, move this to a separate module or function later)
with open("app/data/mock_events.json", "r") as f:
    mock_events = SearchResults.parse_raw(f.read()).events

search_store = {}


@router.post("/searches", response_model=SearchResponse, status_code=201)
def create_search(search_request: SearchRequest):
    search_id = str(uuid4())
    search_store[search_id] = mock_events
    return SearchResponse(search_id=search_id, record_count=len(mock_events))


@router.get("/searches/{search_id}", status_code=204)
def get_search(search_id: str):
    if search_id not in search_store:
        raise HTTPException(status_code=404, detail="Search not found")


@router.get("/searches/{search_id}/results", response_model=SearchResults)
def get_search_results(search_id: str):
    if search_id not in search_store:
        raise HTTPException(status_code=404, detail="Search not found")
    return SearchResults(events=search_store[search_id])

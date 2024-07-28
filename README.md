# Mock Asynchronous Search API
A Mock API for IBM QRadar using FastAPI. This can be used to mock any api which uses an asynchronous search mechanism, meaning takes a search criteria was a parameter and returns a search_id, requires polling using the search id and finally pull the results once the search is complete.

# QRadar Mock Ariel Search API

This project provides a mock API that simulates the QRadar Ariel Search API. It's designed for development and testing purposes, allowing you to experiment with QRadar search functionalities without needing a live QRadar environment.

## Project Layout
```
qradar_mock_api/
├── app/
│   ├── __init__.py         
│   ├── main.py               (Main FastAPI application)
│   ├── models.py             (Pydantic models - Event, SearchRequest, etc.)
│   ├── routers/
│   │   ├── __init__.py    
│   │   └── searches.py       (API router for search endpoints)
│   └── data/
│       └── mock_events.json  (Mock event data)
├── tests/
│   ├── __init__.py         
│   └── test_searches.py      (Test cases for the API)
├── README.md                 (Project description and instructions)
├── pyproject.toml            (Project dependencies)
```

## Features

- **Search Creation:** Create simulated Ariel searches using AQL queries.
- **Search Results:** Retrieve mock search results in the QRadar event format.
- **Customizable:** Easily modify the mock event data in `app/data/mock_events.json` to fit your specific testing scenarios.
- **FastAPI:** Built with FastAPI for high performance and automatic API documentation.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://your-repository-url/qradar_mock_api.git
    ```

2. **Create a search**
   ```bash
   curl -X POST "http://127.0.0.1:8000/searches" -H "Content-Type: application/json" -d '{"query_expression": "SELECT * FROM events"}'
    ```
3. **Get Search ID:**
    ```bash
    curl "http://127.0.0.1:8000/searches/<search_id>"
    ```

4. **Get Search Results using Search ID:**
    ```bash
    curl "http://127.0.0.1:8000/searches/<search_id>/results"
    ```
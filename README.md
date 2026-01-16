# Task Management API

A minimal REST API for task management built with FastAPI, SQLModel, and SQLite.

## Project Structure

```
TaskAPI/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app instance and endpoints
│   ├── models.py         # SQLModel data models
│   ├── database.py       # Database configuration
│   └── schemas.py        # Pydantic schemas (if needed)
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # Pytest fixtures
│   └── test_tasks.py     # API tests
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

4. Run tests:
```bash
pytest
```

## API Endpoints

- `GET /health` - Health check endpoint

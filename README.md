# FlyRank - Task Management API

Welcome to the Task Management API, the inaugural project developed during the project-based virtual internship at **FlyRank**. This project is built and maintained by the Backend AI Engineering team.

## Overview

This project is a high-performance RESTful API built with **FastAPI** that manages a simple To-Do list. It demonstrates the fundamental concepts of backend development by providing the four standard CRUD operations (Create, Read, Update, Delete) utilizing a robust SQLite database with highly optimized raw SQL queries and custom connection pooling. 

## Features

- **Create**: Add new tasks with a title and an optional description.
- **Read**: Retrieve all available tasks or fetch a specific task by its unique ID.
  - **Search & Sort Filtering**: The GET `/tasks` endpoint supports dynamic query parameters. You can search tasks using `?search=keyword` (matches title or description) and sort them via `?sort_by=title&sort_order=desc` (supports sorting by `id`, `title`, or `completed`).
- **Update**: Modify existing tasks (e.g., mark as completed, update the title or description).
- **Delete**: Remove tasks from the system.
- **Raw SQLite with Connection Pooling**: Designed for raw speed and control. Features a custom native Python `queue.Queue` connection pool and completely mitigates SQL injection using parameterized queries (`?`) and strict whitelisting. Database indexes are initialized automatically on startup for maximum read performance.

## Project Structure (Clean Architecture)

The codebase has been refactored for maintainability and separation of concerns:

```
flyrank-fastapi/
│
├── main.py                # Main application entrypoint and app configuration
├── flyrank.db             # Auto-generated SQLite database file
├── models/
│   └── schemas.py         # Data validation schemas (Pydantic models)
├── database/
│   └── database.py        # Custom SQLite connection pooling and initialization logic
└── routes/
    └── routes.py          # API endpoints executing secure raw SQL operations
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- FastAPI
- Uvicorn

### Installation

1. Clone the repository and navigate into the project directory:
   ```bash
   git clone https://github.com/ahmadammarm/flyrank-fastapi.git
   cd flyrank-fastapi
   ```

2. Set up a virtual environment (recommended):
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the API

Start the local development server:

```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`. The `flyrank.db` file alongside optimized indexes will be automatically generated upon startup.

### Interactive Documentation (Swagger UI)

FastAPI automatically generates interactive API documentation. Once the server is running, you can visually test all the endpoints directly from your browser:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---
*Developed by the Backend AI Engineering Intern at FlyRank.*

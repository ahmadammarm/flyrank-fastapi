# FlyRank - Task Management API

Welcome to the Task Management API, the inaugural project developed during the project-based virtual internship at **FlyRank**. This project is built and maintained by the Backend AI Engineering team.

## Overview

This project is a small, lightweight RESTful API built with **FastAPI** that manages a simple To-Do list. It demonstrates the fundamental concepts of backend development by providing the four standard CRUD operations (Create, Read, Update, Delete) utilizing an in-memory data structure. 

## Features

- **Create**: Add new tasks with a title and an optional description.
- **Read**: Retrieve all available tasks or fetch a specific task by its unique ID.
- **Update**: Modify existing tasks (e.g., mark as completed, update the title or description).
- **Delete**: Remove tasks from the system.
- **In-Memory Storage**: Runs out of the box without requiring external database setups.

## Project Structure (Clean Architecture)

The codebase has been refactored for maintainability and separation of concerns:

```
flyrank-fastapi/
│
├── main.py                # Main application entrypoint and app configuration
├── models/
│   └── models.py          # Data validation schemas (Pydantic models)
├── database/
│   └── database.py        # In-memory data store logic and CRUD implementation
└── routes/
    └── routes.py          # API endpoints and request routing
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- FastAPI
- Uvicorn

### Installation

1. Clone the repository and navigate into the project directory:
   ```bash
   git clone <your-repo-url>
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
   pip install fastapi uvicorn
   ```

### Running the API

Start the local development server:

```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

### Interactive Documentation (Swagger UI)

FastAPI automatically generates interactive API documentation. Once the server is running, you can visually test all the endpoints directly from your browser:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---
*Developed by the Backend AI Engineering Intern at FlyRank.*

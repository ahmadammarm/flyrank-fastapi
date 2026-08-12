# FlyRank - Task Management API

Welcome to the Task Management API, the inaugural project developed during the project-based virtual internship at **FlyRank**. This project is built and maintained by the Backend AI Engineering team.

## Overview

This project is a high-performance RESTful API built with **FastAPI** that manages a simple To-Do list. It demonstrates the fundamental concepts of backend development by providing the four standard CRUD operations (Create, Read, Update, Delete) utilizing a robust **PostgreSQL** database running in Docker.
## Features

- **Create**: Add new tasks with a title and an optional description.
- **Read**: Retrieve all available tasks or fetch a specific task by its unique ID.
  - **Search & Sort Filtering**: The GET `/tasks` endpoint supports dynamic query parameters. You can search tasks using `?search=keyword` (matches title or description) and sort them via `?sort_by=title&sort_order=desc` (supports sorting by `id`, `title`, or `completed`).
- **Update**: Modify existing tasks (e.g., mark as completed, update the title or description).
- **Delete**: Remove tasks from the system.
- **Dockerized PostgreSQL**: Designed for production-readiness. The application and database are orchestrated using Docker Compose. A Postgres repository seamlessly replaced the in-memory/SQLite one. **Crucially, the service and routes remained completely unchanged**—proving the effectiveness of the architecture. Database initialization and indexing are handled automatically on startup.
## Project Structure (Clean Architecture)

The codebase has been refactored for maintainability and separation of concerns:

```
flyrank-fastapi/
│
├── main.py                # Main application entrypoint and app configuration
├── docker-compose.yml     # Docker orchestration for app and PostgreSQL
├── Dockerfile             # Container definition for the FastAPI app
├── .env.example           # Example environment variables (gitignored .env used for connection strings)
├── models/
│   └── schemas.py         # Data validation schemas (Pydantic models)
├── database/
│   ├── database.py        # Database connection pool and SQLite-to-Postgres wrapper
│   └── init.sql           # SQL script to initialize tables on Docker volume creation
└── routes/
    └── routes.py          # API endpoints executing secure raw SQL operations
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

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

3. Create your local environment variables:
   ```bash
   cp .env.example .env
   ```

### Running the Stack

Start the local development server and database using Docker Compose:

```bash
docker compose up -d
```

The API will be available at `http://localhost:8000`. The PostgreSQL database will run on port `5432` with a persistent volume.

### Architecture & Persistence Proof

- **Architecture Proof**: The underlying database was successfully migrated from an in-memory/SQLite implementation to a fully Dockerized PostgreSQL instance. To achieve this, the `database.py` file was updated with a psycopg2 connection wrapper that translates SQLite syntax (`?`) to Postgres (`%s`) and handles returning inserted IDs. As required, **the service and routes remained entirely unchanged**, proving that the architecture effectively isolates the data storage implementation.
- **Persistence Proof**: Data persistence is guaranteed via a Docker volume (`pgdata`). This was proven by:
  1. Running `docker compose up -d`.
  2. Creating new tasks via the API (`POST /tasks`).
  3. Stopping and removing the containers using `docker compose down`.
  4. Restarting the stack with `docker compose up -d`.
  5. Fetching the tasks (`GET /tasks`) to confirm the created rows were still intact.

### Interactive Documentation (Swagger UI)

FastAPI automatically generates interactive API documentation. Once the server is running, you can visually test all the endpoints directly from your browser:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Database Screenshot
<img width="1008" height="317" alt="image" src="https://github.com/user-attachments/assets/68caf8fa-15c4-4f09-82f1-398e7ab970d0" />


---
*Developed by the Backend AI Engineering Intern at FlyRank.*

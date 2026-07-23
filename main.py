from fastapi import FastAPI
from routes.routes import router as task_router
from database.database import init_db

# Create database tables and indexes on startup
init_db()

app = FastAPI(
    title="To-Do API",
    description="A small API that manages a to-do list using raw SQLite queries",
    version="1.0.0"
)

app.include_router(task_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the To-Do API", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routes.routes import router as task_router
from database.database import init_db

# Create database tables and indexes on startup
init_db()

app = FastAPI(
    title="To-Do API",
    description="A small API that manages a to-do list using raw SQLite queries",
    version="1.0.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )

app.include_router(task_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the To-Do API", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
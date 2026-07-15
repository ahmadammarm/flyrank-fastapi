from fastapi import FastAPI
from routes.routes import router as task_router

app = FastAPI(
    title="To-Do API",
    description="A small API that manages a to-do list",
    version="1.0.0"
)

app.include_router(task_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the To-Do API", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

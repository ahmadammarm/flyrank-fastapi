from fastapi import FastAPI, Depends, HTTPException, status
from typing import List

from database.database import init_db, get_db
from models.schemas import DocumentCreate, DocumentResponse, ChatRequest, ChatResponse, FeedbackRequest
from core.document_management import ingest_document
from core.conversation_workflows import process_chat_request, get_chat_history
from core import crud

# Initialize Database
init_db()

app = FastAPI(
    title="CivicRAG API",
    description="A Retrieval-Augmented Generation API for Civic & Tenant Rights using PostgreSQL and pgvector",
    version="2.0.0"
)

# 1. System Health
@app.get("/system/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "service": "CivicRAG API"}

# 2. System Stats
@app.get("/system/stats", tags=["System"])
async def get_stats(db = Depends(get_db)):
    docs, sessions = crud.get_system_stats(db)
    return {"documents": docs, "chat_sessions": sessions}

# 3. Ingest Document
@app.post("/documents/", response_model=dict, tags=["Documents"])
async def create_document(doc: DocumentCreate, db = Depends(get_db)):
    doc_id = ingest_document(db, doc.title, doc.content)
    return {"message": "Document ingested successfully", "id": doc_id}

# 4. List Documents
@app.get("/documents/", response_model=List[DocumentResponse], tags=["Documents"])
async def list_documents(db = Depends(get_db)):
    return crud.get_all_documents(db)

# 5. Get Document
@app.get("/documents/{doc_id}", tags=["Documents"])
async def get_document(doc_id: int, db = Depends(get_db)):
    doc = crud.get_document_by_id(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

# 6. Delete Document
@app.delete("/documents/{doc_id}", tags=["Documents"])
async def delete_document(doc_id: int, db = Depends(get_db)):
    crud.delete_document_by_id(db, doc_id)
    return {"message": "Document deleted"}

# 7. Start/Continue Chat
@app.post("/chat/", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest, db = Depends(get_db)):
    session_id = request.session_id
    if not session_id:
        session_id = crud.create_chat_session(db)
        
    reply = process_chat_request(db, session_id, request.message)
    return {"session_id": session_id, "reply": reply}

# 8. List Chat Sessions
@app.get("/chat/sessions", tags=["Chat"])
async def list_sessions(db = Depends(get_db)):
    return crud.get_all_chat_sessions(db)

# 9. Get Chat History
@app.get("/chat/sessions/{session_id}", tags=["Chat"])
async def session_history(session_id: int, db = Depends(get_db)):
    return get_chat_history(db, session_id)

# 10. Delete Chat Session
@app.delete("/chat/sessions/{session_id}", tags=["Chat"])
async def delete_session(session_id: int, db = Depends(get_db)):
    crud.delete_chat_session(db, session_id)
    return {"message": "Session deleted"}

# 11. Chat Feedback
@app.post("/chat/feedback", tags=["Chat"])
async def submit_feedback(feedback: FeedbackRequest, db = Depends(get_db)):
    crud.save_chat_feedback(db, feedback.message_id, feedback.is_positive, feedback.comments)
    return {"message": "Feedback saved"}
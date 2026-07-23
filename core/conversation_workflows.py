from .retrieval_pipelines import retrieve_relevant_chunks
from .llm_orchestration import generate_rag_response

def get_chat_history(db, session_id: int):
    cursor = db.cursor()
    cursor.execute("SELECT role, content FROM chat_messages WHERE session_id = %s ORDER BY created_at ASC", (session_id,))
    rows = cursor.fetchall()
    return [{"role": row["role"], "content": row["content"]} for row in rows]

def save_message(db, session_id: int, role: str, content: str):
    cursor = db.cursor()
    cursor.execute("INSERT INTO chat_messages (session_id, role, content) VALUES (%s, %s, %s) RETURNING id", (session_id, role, content))
    db.commit()
    return cursor.fetchone()['id']

def process_chat_request(db, session_id: int, message: str) -> str:
    # 1. Retrieve relevant context
    context = retrieve_relevant_chunks(db, message)
    
    # 2. Get history
    history = get_chat_history(db, session_id)
    
    # 3. Generate response
    # Map 'user'/'assistant' to 'user'/'model' for gemini
    gemini_history = []
    for msg in history:
        gemini_history.append({"role": "model" if msg["role"] == "assistant" else "user", "content": msg["content"]})
        
    ai_reply = generate_rag_response(message, context, gemini_history)
    
    # 4. Save to db
    save_message(db, session_id, "user", message)
    save_message(db, session_id, "assistant", ai_reply)
    
    return ai_reply

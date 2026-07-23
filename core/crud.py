def get_system_stats(db):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM documents")
    docs = cursor.fetchone()['count']
    cursor.execute("SELECT COUNT(*) FROM chat_sessions")
    sessions = cursor.fetchone()['count']
    return docs, sessions

def get_all_documents(db):
    cursor = db.cursor()
    cursor.execute("SELECT id, title, created_at FROM documents")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

def get_document_by_id(db, doc_id: int):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM documents WHERE id = %s", (doc_id,))
    row = cursor.fetchone()
    return dict(row) if row else None

def delete_document_by_id(db, doc_id: int):
    cursor = db.cursor()
    cursor.execute("DELETE FROM documents WHERE id = %s", (doc_id,))
    db.commit()

def create_chat_session(db, session_name: str = 'New Session') -> int:
    cursor = db.cursor()
    cursor.execute("INSERT INTO chat_sessions (session_name) VALUES (%s) RETURNING id", (session_name,))
    db.commit()
    return cursor.fetchone()['id']

def get_all_chat_sessions(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM chat_sessions")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

def delete_chat_session(db, session_id: int):
    cursor = db.cursor()
    cursor.execute("DELETE FROM chat_sessions WHERE id = %s", (session_id,))
    db.commit()

def save_chat_feedback(db, message_id: int, is_positive: bool, comments: str):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO chat_feedback (message_id, is_positive, comments) VALUES (%s, %s, %s)",
        (message_id, is_positive, comments)
    )
    db.commit()

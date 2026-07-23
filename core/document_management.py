import json
from .retrieval_pipelines import get_embedding

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def ingest_document(db, title: str, content: str):
    cursor = db.cursor()
    cursor.execute("INSERT INTO documents (title, content) VALUES (%s, %s) RETURNING id", (title, content))
    doc_id = cursor.fetchone()['id']
    
    chunks = chunk_text(content)
    chunk_data = []
    
    for chunk in chunks:
        embedding = get_embedding(chunk)
        # We pass the list as a JSON string, which PostgreSQL casts to vector via %s::vector
        chunk_data.append((doc_id, chunk, json.dumps(embedding)))
        
    cursor.executemany(
        "INSERT INTO document_chunks (document_id, text_chunk, embedding) VALUES (%s, %s, %s::vector)",
        chunk_data
    )
    db.commit()
    return doc_id

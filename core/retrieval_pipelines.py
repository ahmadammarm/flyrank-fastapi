import google.generativeai as genai
import os
import json
from typing import List

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY", "dummy_key")
genai.configure(api_key=api_key)

def get_embedding(text: str) -> List[float]:
    try:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        return [0.0] * 768

def retrieve_relevant_chunks(db, query: str, top_k: int = 3) -> List[str]:
    query_embedding = get_embedding(query)
    query_embedding_str = json.dumps(query_embedding)
    
    cursor = db.cursor()
    # pgvector '<=>' operator computes cosine distance. We order by distance ASC.
    sql = """
        SELECT text_chunk 
        FROM document_chunks 
        ORDER BY embedding <=> %s::vector 
        LIMIT %s
    """
    cursor.execute(sql, (query_embedding_str, top_k))
    rows = cursor.fetchall()
    
    return [row['text_chunk'] for row in rows]

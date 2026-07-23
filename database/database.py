import os
import psycopg2
from psycopg2 import pool
from typing import Generator
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/civicrag")

try:
    db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, DATABASE_URL)
except Exception as e:
    print("Database connection failed. Ensure PostgreSQL is running.")
    db_pool = None

def init_db():
    if not db_pool:
        return
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        
        # Enable pgvector extension
        cursor.execute('CREATE EXTENSION IF NOT EXISTS vector;')
        
        # Documents Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Document Chunks Table with vector type (Gemini is 768 dimensions)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_chunks (
                id SERIAL PRIMARY KEY,
                document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
                text_chunk TEXT NOT NULL,
                embedding vector(768) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Chat Sessions Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id SERIAL PRIMARY KEY,
                session_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Chat Messages Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id SERIAL PRIMARY KEY,
                session_id INTEGER REFERENCES chat_sessions(id) ON DELETE CASCADE,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Feedback Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_feedback (
                id SERIAL PRIMARY KEY,
                message_id INTEGER REFERENCES chat_messages(id) ON DELETE CASCADE,
                is_positive BOOLEAN,
                comments TEXT
            )
        ''')
        
        # Add index for vector similarity (HNSW index for cosine distance)
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS document_chunks_embedding_idx 
            ON document_chunks USING hnsw (embedding vector_cosine_ops);
        ''')
        
        conn.commit()
    finally:
        db_pool.putconn(conn)

def get_db() -> Generator:
    if not db_pool:
        raise Exception("Database connection pool is not initialized")
    conn = db_pool.getconn()
    conn.cursor_factory = RealDictCursor
    try:
        yield conn
    finally:
        db_pool.putconn(conn)

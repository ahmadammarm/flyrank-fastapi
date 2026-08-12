import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Generator
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/flyrank")

class PostgresCursorWrapper:
    """
    A wrapper to translate SQLite syntax/behavior to PostgreSQL
    so that the routes/service layer does not need to change.
    """
    def __init__(self, pg_cursor):
        self.pg_cursor = pg_cursor
        self.lastrowid = None

    def execute(self, query, params=()):
        # Translate SQLite '?' to Postgres '%s'
        pg_query = query.replace('?', '%s')
        
        # Handle SQLite's lastrowid for INSERTs
        is_insert = pg_query.strip().upper().startswith("INSERT")
        if is_insert and "RETURNING" not in pg_query:
            pg_query += " RETURNING id"
            
        self.pg_cursor.execute(pg_query, params)
        
        if is_insert:
            row = self.pg_cursor.fetchone()
            if row:
                self.lastrowid = row['id']
                
    def fetchone(self):
        return self.pg_cursor.fetchone()
        
    def fetchall(self):
        return self.pg_cursor.fetchall()

class PostgresConnectionWrapper:
    """
    Mocks the sqlite3.Connection interface.
    """
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn
        
    def cursor(self):
        # RealDictCursor allows dict(row) to work just like sqlite3.Row
        return PostgresCursorWrapper(self.pg_conn.cursor(cursor_factory=RealDictCursor))
        
    def commit(self):
        self.pg_conn.commit()
        
    def close(self):
        self.pg_conn.close()

def init_db():
    # Database is now initialized via docker-compose (init.sql)
    # We leave this function here so main.py doesn't break
    pass

def get_db() -> Generator:
    conn = psycopg2.connect(DATABASE_URL)
    wrapper = PostgresConnectionWrapper(conn)
    try:
        yield wrapper
    finally:
        conn.close()

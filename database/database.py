import sqlite3
import queue
from typing import Generator

DATABASE_URL = "./flyrank.db"

class SQLiteConnectionPool:
    def __init__(self, database: str, pool_size: int = 5):
        self.database = database
        self.pool_size = pool_size
        self.pool = queue.Queue(maxsize=pool_size)
        
        # Initialize the pool with connections
        for _ in range(pool_size):
            self.pool.put(self._create_connection())

    def _create_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.database, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def get_connection(self) -> sqlite3.Connection:
        try:
            # Wait up to 5 seconds for an available connection
            return self.pool.get(timeout=5)
        except queue.Empty:
            raise Exception("Database connection pool exhausted")

    def release_connection(self, conn: sqlite3.Connection):
        try:
            self.pool.put_nowait(conn)
        except queue.Full:
            # If the pool is somehow full, close the extra connection
            conn.close()

# Create a global connection pool instance
db_pool = SQLiteConnectionPool(DATABASE_URL, pool_size=5)

def init_db():
    conn = db_pool.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        # Add indexes for query optimization
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_title ON tasks(title)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed)')
        
        # Insert three example tasks on first run
        cursor.execute("SELECT COUNT(*) FROM tasks")
        if cursor.fetchone()[0] == 0:
            example_tasks = [
                ("Learn FastAPI", "Study the FastAPI documentation", False),
                ("Setup SQLite", "Configure raw queries and connection pooling", True),
                ("Deploy to GitHub", "Push the final code to the repository", False)
            ]
            cursor.executemany("INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)", example_tasks)
            
        conn.commit()
    finally:
        db_pool.release_connection(conn)

# FastAPI Dependency for connection pooling
def get_db() -> Generator:
    conn = db_pool.get_connection()
    try:
        yield conn
    finally:
        db_pool.release_connection(conn)

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_tasks_title ON tasks(title);
CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed);

-- Insert example tasks if table is empty
INSERT INTO tasks (title, description, completed)
SELECT 'Learn FastAPI', 'Study the FastAPI documentation', FALSE
WHERE NOT EXISTS (SELECT 1 FROM tasks);

INSERT INTO tasks (title, description, completed)
SELECT 'Setup Postgres', 'Configure docker and persistence', TRUE
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE title = 'Setup Postgres');

INSERT INTO tasks (title, description, completed)
SELECT 'Deploy to GitHub', 'Push the final code to the repository', FALSE
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE title = 'Deploy to GitHub');

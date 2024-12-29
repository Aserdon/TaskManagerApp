-- Table to store tasks
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,           -- Unique identifier for the task
    content TEXT NOT NULL,                          -- Content of the task
    completed BOOLEAN NOT NULL DEFAULT 0,           -- Flag to indicate if the task is completed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the task was created
    completed_at TIMESTAMP                          -- Timestamp when the task was completed
);

-- Index to speed up queries by created_at
CREATE INDEX IF NOT EXISTS idx_created_at ON tasks (created_at);

-- Index to speed up queries by completed_at
CREATE INDEX IF NOT EXISTS idx_completed_at ON tasks (completed_at);
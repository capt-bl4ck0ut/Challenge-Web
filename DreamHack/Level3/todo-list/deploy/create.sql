-- Users
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- TodoList
CREATE TABLE IF NOT EXISTS Todolist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

-- Todo
CREATE TABLE IF NOT EXISTS Todo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    todo_list_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    is_completed BOOLEAN NOT NULL DEFAULT 0,
    start_date DATE,
    due_date DATE,
    FOREIGN KEY (todo_list_id) REFERENCES Todolist(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TodoShares (
    todo_id INTEGER,
    user_id INTEGER,
    permission_type TEXT,  -- 'owner', 'shared'
    PRIMARY KEY (todo_id, user_id),
    FOREIGN KEY (todo_id) REFERENCES Todo(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

INSERT INTO Users (username, email, password) VALUES (
    'admin',
    'admin@dreamhack.io',
    'helloworld' -- redacted
);
INSERT INTO Todolist (user_id, name) VALUES (
    1,
    'admin'
);

INSERT INTO Todo (todo_list_id, title, description, is_completed) VALUES (
    1,
    'flag',
    'DH{sample_flag}',
    1
);

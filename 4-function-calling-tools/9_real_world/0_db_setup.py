"""
Setup: Create Small Database
=============================
Creates a simple tasks database for real-world demonstrations.
 
Tables: users, tasks
Data: Simple task management data
"""
 
import sqlite3
 
# Create SQLite database (no server needed!)
print("📦 Creating tasks.db...")
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()
 
# Drop existing tables
cursor.execute("DROP TABLE IF EXISTS tasks")
cursor.execute("DROP TABLE IF EXISTS users")
 
# Create tables
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT
)
""")
 
cursor.execute("""
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT NOT NULL,
    status TEXT,
    created_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")
 
# Insert sample data
users = [
    (1, "Alice Johnson", "alice@example.com"),
    (2, "Bob Smith", "bob@example.com"),
    (3, "Carol White", "carol@example.com")
]
cursor.executemany("INSERT INTO users VALUES (?, ?, ?)", users)
 
tasks = [
    (1, 1, "Write documentation", "completed", "2024-01-15"),
    (2, 1, "Review code", "pending", "2024-01-16"),
    (3, 2, "Fix bug #123", "in_progress", "2024-01-14"),
    (4, 2, "Update tests", "pending", "2024-01-17"),
    (5, 3, "Deploy to production", "completed", "2024-01-10"),
    (6, 3, "Monitor metrics", "pending", "2024-01-18")
]
cursor.executemany("INSERT INTO tasks VALUES (?, ?, ?, ?, ?)", tasks)
 
conn.commit()
 
# Verify
print("✅ Database created: tasks.db")
print("\nData Summary:")
cursor.execute("SELECT COUNT(*) FROM users")
print(f"  Users: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM tasks")
print(f"  Tasks: {cursor.fetchone()[0]}")
 
print("\nSample Tasks:")
cursor.execute("SELECT users.name, tasks.title, tasks.status FROM tasks JOIN users ON tasks.user_id = users.id LIMIT 3")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} ({row[2]})")
 
conn.close()
print("\n✅ Setup complete! Run numbered examples to see tools in action.")
import sqlite3

# Conectare și inițializare bază de date
def connect_db():
    conn = sqlite3.connect('task_planner.db')
    cursor = conn.cursor()

    # Creăm tabelul tasks cu coloana subcategory inclusă
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            subcategory TEXT,  -- Adăugăm coloana subcategory
            due_date TEXT,
            priority TEXT,
            status TEXT,
            reminder TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    return conn

def add_task(title, description, category, subcategory, due_date, priority, status, reminder):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, category, subcategory, due_date, priority, status, reminder)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, description, category, subcategory, due_date, priority, status, reminder))
    conn.commit()
    conn.close()

def get_tasks(filter_by=None, search_query=None):
    conn = connect_db()
    cursor = conn.cursor()

    if filter_by:
        cursor.execute(f"SELECT * FROM tasks WHERE status = ?", (filter_by,))
    elif search_query:
        cursor.execute(f"SELECT * FROM tasks WHERE title LIKE ?", (f"%{search_query}%",))
    else:
        cursor.execute("SELECT * FROM tasks")
    
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def update_task(task_id, title, description, category, subcategory, due_date, priority, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks
        SET title = ?, description = ?, category = ?, subcategory = ?, due_date = ?, priority = ?, status = ?
        WHERE id = ?
    ''', (title, description, category, subcategory, due_date, priority, status, task_id))
    conn.commit()
    conn.close()

def archive_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO archived_tasks SELECT * FROM tasks WHERE id = ?
    ''', (task_id,))
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def get_task_statistics():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Finalizat'")
    completed_tasks = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'În curs'")
    pending_tasks = cursor.fetchone()[0]
    
    conn.close()
    return {
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks
    }

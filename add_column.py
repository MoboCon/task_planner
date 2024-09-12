import sqlite3

def add_subcategory_column():
    conn = sqlite3.connect('task_planner.db')
    cursor = conn.cursor()

    # Adăugăm coloana subcategory dacă nu există deja
    try:
        cursor.execute('''
            ALTER TABLE tasks ADD COLUMN subcategory TEXT;
        ''')
        conn.commit()
        print("Coloana 'subcategory' a fost adăugată cu succes.")
    except sqlite3.OperationalError as e:
        print(f"Eroare: {e}")

    conn.close()

if __name__ == "__main__":
    add_subcategory_column()

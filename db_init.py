import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

   
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            book_id TEXT
        )
    """)

   

    conn.commit()
    conn.close()
    print("Database initialized!")

if __name__ == "__main__":
    init_db()

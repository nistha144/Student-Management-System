import sqlite3
from werkzeug.security import generate_password_hash


def get_db_connection():
    connection = sqlite3.connect("database/attendance.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()
def create_attendance_table():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            attendance_date TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Present', 'Absent')),
            UNIQUE(student_id, subject_id, attendance_date),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        )
    """)

    connection.commit()
    connection.close()    

def add_test_users():
    connection = get_db_connection()

    connection.execute("""
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, (
        "teacher",
        generate_password_hash("teacher123"),
        "teacher"
    ))

    connection.execute("""
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, (
        "student",
        generate_password_hash("student123"),
        "student"
    ))

    connection.commit()
    connection.close()
if __name__ == "__main__":
    create_tables()
    create_attendance_table()
    add_test_users()
    print("Database and users table created successfully!")
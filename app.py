from flask import Flask, request
from database import get_db_connection

app = Flask(__name__)


@app.route("/")
def home():
    return "Student Attendance System is Running!"

@app.route("/students")
def students():
    connection = get_db_connection()
    students = connection.execute("SELECT * FROM students").fetchall()
    connection.close()

    return str([dict(Student)for Student in students])
@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        student_id = request.form["student_id"]
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO students (student_id, name, email, phone)
            VALUES (?, ?, ?, ?)
        """, (student_id, name, email, phone))

        connection.commit()
        connection.close()

        return "Student added successfully!"

    return """
        <h2>Add Student</h2>

        <form method="POST">
            Student ID: <input type="text" name="student_id"><br><br>
            Name: <input type="text" name="name"><br><br>
            Email: <input type="text" name="email"><br><br>
            Phone: <input type="text" name="phone"><br><br>

            <input type="submit" value="Add Student">
        </form>
    """   
@app.route("/edit_student/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    connection = get_db_connection()

    if request.method == "POST":
        student_id = request.form["student_id"]
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        connection.execute("""
            UPDATE students
            SET student_id = ?, name = ?, email = ?, phone = ?
            WHERE id = ?
        """, (student_id, name, email, phone, id))

        connection.commit()
        connection.close()

        return "Student updated successfully!"

    student = connection.execute(
        "SELECT * FROM students WHERE id = ?", (id,)
    ).fetchone()

    connection.close()

    return f"""
        <h2>Edit Student</h2>

        <form method="POST">
            Student ID:
            <input type="text" name="student_id" value="{student['student_id']}"><br><br>

            Name:
            <input type="text" name="name" value="{student['name']}"><br><br>

            Email:
            <input type="text" name="email" value="{student['email']}"><br><br>

            Phone:
            <input type="text" name="phone" value="{student['phone']}"><br><br>

            <input type="submit" value="Update Student">
        </form>
    """

@app.route("/subjects")
def subjects():
    connection = get_db_connection()
    subjects = connection.execute("SELECT * FROM subjects").fetchall()
    connection.close()

    return str([dict(subject) for subject in subjects])

@app.route("/add_subject", methods=["GET", "POST"])
def add_subject():
    if request.method == "POST":
        subject_id = request.form["subject_id"]
        subject_name = request.form["subject_name"]

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO subjects (subject_id, subject_name)
            VALUES (?, ?)
        """, (subject_id, subject_name))

        connection.commit()
        connection.close()

        return "Subject added successfully!"

    return """
        <h2>Add Subject</h2>

        <form method="POST">
            Subject ID:
            <input type="text" name="subject_id"><br><br>

            Subject Name:
            <input type="text" name="subject_name"><br><br>

            <input type="submit" value="Add Subject">
        </form>
    """

@app.route("/edit_subject/<int:id>", methods=["GET", "POST"])
def edit_subject(id):
    connection = get_db_connection()

    if request.method == "POST":
        subject_id = request.form["subject_id"]
        subject_name = request.form["subject_name"]

        connection.execute("""
            UPDATE subjects
            SET subject_id = ?, subject_name = ?
            WHERE id = ?
        """, (subject_id, subject_name, id))

        connection.commit()
        connection.close()

        return "Subject updated successfully!"

    subject = connection.execute(
        "SELECT * FROM subjects WHERE id = ?", (id,)
    ).fetchone()

    connection.close()

    return f"""
        <h2>Edit Subject</h2>

        <form method="POST">
            Subject ID:
            <input type="text" name="subject_id" value="{subject['subject_id']}"><br><br>

            Subject Name:
            <input type="text" name="subject_name" value="{subject['subject_name']}"><br><br>

            <input type="submit" value="Update Subject">
        </form>
    """

if __name__ == "__main__":
    app.run(debug=True)
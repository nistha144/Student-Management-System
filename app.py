
from flask import Flask, request
from database import get_db_connection

app = Flask(__name__)


# HOME PAGE


@app.route("/")
def home():
    connection = get_db_connection()

    total_students = connection.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    total_subjects = connection.execute(
        "SELECT COUNT(*) FROM subjects"
    ).fetchone()[0]

    connection.close()

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Management System</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f0f4f8;
                margin: 0;
                text-align: center;
            }}
            header {{
                background: #1e3a8a;
                color: white;
                padding: 30px;
            }}
            .container {{
                margin: 40px auto;
                max-width: 850px;
            }}
            .card {{
                display: inline-block;
                background: white;
                width: 250px;
                margin: 15px;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 3px 10px #cccccc;
            }}
            .count {{
                font-size: 40px;
                color: #2563eb;
                font-weight: bold;
            }}
            .card h2 {{
                color: #1e3a8a;
            }}
            a {{
                display: inline-block;
                background: #2563eb;
                color: white;
                padding: 12px 20px;
                text-decoration: none;
                border-radius: 6px;
                margin-top: 10px;
            }}
            footer {{
                margin-top: 40px;
                padding: 15px;
                color: #555;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Student Management System</h1>
            <p>Manage Students and Subjects Easily</p>
        </header>

        <div class="container">
            <div class="card">
                <h2>Total Students</h2>
                <div class="count">{total_students}</div>
                <a href="/students">View Students</a>
            </div>

            <div class="card">
                <h2>Total Subjects</h2>
                <div class="count">{total_subjects}</div>
                <a href="/subjects">View Subjects</a>
            </div>

            <div class="card">
                <h2>Add Student</h2>
                <p>Register a new student</p>
                <a href="/add_student">Add Student</a>
            </div>

            <div class="card">
                <h2>Add Subject</h2>
                <p>Add a new subject</p>
                <a href="/add_subject">Add Subject</a>
            </div>
        </div>

        <footer>
            Student Management System | Project Dashboard
        </footer>
    </body>
    </html>
    """




# STUDENTS LIST


@app.route("/students")
def students():
    search = request.args.get("search", "").strip()

    connection = get_db_connection()

    if search:
        students = connection.execute("""
            SELECT * FROM students
            WHERE name LIKE ? OR student_id LIKE ?
        """, (f"%{search}%", f"%{search}%")).fetchall()
    else:
        students = connection.execute(
            "SELECT * FROM students"
        ).fetchall()

    connection.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Students List</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f0f4f8;
                margin: 0;
                padding: 30px;
            }

            h1 {
                color: #1e3a8a;
                text-align: center;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                background: white;
                margin-top: 25px;
            }

            th, td {
                padding: 14px;
                border: 1px solid #ddd;
                text-align: center;
            }

            th {
                background: #1e3a8a;
                color: white;
            }

            tr:nth-child(even) {
                background: #f2f2f2;
            }

            a, button {
                display: inline-block;
                padding: 9px 13px;
                border: none;
                border-radius: 5px;
                text-decoration: none;
                color: white;
                cursor: pointer;
                margin: 3px;
            }

            .edit { background: #2563eb; }
            .delete { background: #dc2626; }
            .add { background: #15803d; }
            .home { background: #475569; }
            .search-btn { background: #2563eb; }

            .search-box {
                padding: 11px;
                width: 250px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        </style>
    </head>

    <body>

        <h1>Students List</h1>

        <a class="add" href="/add_student">Add New Student</a>
        <a class="home" href="/">Home</a>

        <br><br>

        <form method="GET" action="/students">
            <input class="search-box" type="text"
                   name="search"
                   placeholder="Search by Name or Student ID"
                   value="SEARCH_VALUE">

            <button class="search-btn" type="submit">Search</button>
            <a class="home" href="/students">Reset</a>
        </form>

        <table>
            <tr>
                <th>ID</th>
                <th>Student ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Actions</th>
            </tr>
    """.replace("SEARCH_VALUE", search.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;"))

    if not students:
        html += """
        <tr>
            <td colspan="6">No students found!</td>
        </tr>
        """

    for student in students:
        html += f"""
            <tr>
                <td>{student['id']}</td>
                <td>{student['student_id']}</td>
                <td>{student['name']}</td>
                <td>{student['email']}</td>
                <td>{student['phone']}</td>
                <td>
                    <a class="edit" href="/edit_student/{student['id']}">Edit</a>
                    <a class="edit" href="/student_details/{student['id']}">Details</a>
                    <form action="/delete_student/{student['id']}"
                          method="POST" style="display:inline;"
                          onsubmit="return confirm('Delete this student?');">
                        <button class="delete" type="submit">Delete</button>
                    </form>
                </td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html




# ADD STUDENT

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

        return """
        <h2>Student added successfully!</h2>
        <a href="/students">View Students</a>
        <a href="/">Home</a>
        """

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Student</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f0f4f8;
                margin: 0;
                padding: 30px;
            }

            .container {
                background: white;
                max-width: 450px;
                margin: 40px auto;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 3px 12px #cccccc;
            }

            h2 {
                text-align: center;
                color: #1e3a8a;
            }

            label {
                display: block;
                margin-top: 15px;
                font-weight: bold;
            }

            input {
                width: 100%;
                padding: 12px;
                margin-top: 7px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 6px;
            }

            button {
                width: 100%;
                background: #2563eb;
                color: white;
                padding: 13px;
                border: none;
                border-radius: 6px;
                margin-top: 25px;
                cursor: pointer;
                font-size: 16px;
            }

            button:hover {
                background: #1e40af;
            }

            .back {
                display: block;
                text-align: center;
                margin-top: 20px;
                color: #2563eb;
                text-decoration: none;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h2>Add New Student</h2>

            <form method="POST">

                <label>Student ID</label>
                <input type="text" name="student_id" required>

                <label>Student Name</label>
                <input type="text" name="name" required>

                <label>Email</label>
                <input type="email" name="email">

                <label>Phone</label>
                <input type="text" name="phone">

                <button type="submit">Add Student</button>

            </form>

            <a class="back" href="/">Back to Home</a>

        </div>

    </body>
    </html>
    """



# EDIT STUDENT

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

        return """
        <h2>Student updated successfully!</h2>
        <a href="/students">View Students</a>
        <a href="/">Home</a>
        """

    student = connection.execute(
        "SELECT * FROM students WHERE id = ?", (id,)
    ).fetchone()

    connection.close()

    if student is None:
        return "Student not found!"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Edit Student</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f0f4f8;
                margin: 0;
                padding: 30px;
            }}

            .container {{
                background: white;
                max-width: 450px;
                margin: 40px auto;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 3px 12px #cccccc;
            }}

            h2 {{
                text-align: center;
                color: #1e3a8a;
            }}

            label {{
                display: block;
                margin-top: 15px;
                font-weight: bold;
            }}

            input {{
                width: 100%;
                padding: 12px;
                margin-top: 7px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 6px;
            }}

            button {{
                width: 100%;
                background: #2563eb;
                color: white;
                padding: 13px;
                border: none;
                border-radius: 6px;
                margin-top: 25px;
                cursor: pointer;
                font-size: 16px;
            }}

            button:hover {{
                background: #1e40af;
            }}

            .back {{
                display: block;
                text-align: center;
                margin-top: 20px;
                color: #2563eb;
                text-decoration: none;
            }}
        </style>
    </head>

    <body>
        <div class="container">

            <h2>Edit Student Details</h2>

            <form method="POST">

                <label>Student ID</label>
                <input type="text" name="student_id"
                       value="{student['student_id']}" required>

                <label>Student Name</label>
                <input type="text" name="name"
                       value="{student['name']}" required>

                <label>Email</label>
                <input type="email" name="email"
                       value="{student['email']}">

                <label>Phone</label>
                <input type="text" name="phone"
                       value="{student['phone']}">

                <button type="submit">Update Student</button>

            </form>

            <a class="back" href="/students">Back to Students</a>

        </div>
    </body>
    </html>
    """



# DELETE STUDENT
@app.route("/delete_student/<int:id>", methods=["POST"])
def delete_student(id):
    connection = get_db_connection()
    connection.execute("DELETE FROM students WHERE id = ?", (id,))
    connection.commit()
    connection.close()

    return '<p>Student deleted successfully!</p><a href="/students">Back to Students</a>'


# SUBJECTS LIST


@app.route("/subjects")
def subjects():
    search = request.args.get("search", "").strip()

    connection = get_db_connection()

    if search:
        subjects = connection.execute(
            """SELECT * FROM subjects
               WHERE subject_name LIKE ? OR subject_id LIKE ?""",
            (f"%{search}%", f"%{search}%")
        ).fetchall()
    else:
        subjects = connection.execute(
            "SELECT * FROM subjects"
        ).fetchall()

    connection.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Subjects List</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f0f4f8;
                margin: 0;
                padding: 30px;
            }

            h1 {
                color: #1e3a8a;
                text-align: center;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                background: white;
                margin-top: 25px;
            }

            th, td {
                padding: 14px;
                border: 1px solid #ddd;
                text-align: center;
            }

            th {
                background: #1e3a8a;
                color: white;
            }

            tr:nth-child(even) {
                background: #f2f2f2;
            }

            a, button {
                display: inline-block;
                padding: 9px 13px;
                border: none;
                border-radius: 5px;
                text-decoration: none;
                color: white;
                cursor: pointer;
                margin: 3px;
            }

            .edit {
                background: #2563eb;
            }

            .delete {
                background: #dc2626;
            }

            .add {
                background: #15803d;
            }

            .home {
                background: #475569;
            }

            .search-btn {
                background: #1e3a8a;
            }

            .reset {
                background: #64748b;
            }

            input {
                padding: 10px;
                width: 250px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>

        <h1>Subjects List</h1>

        <a class="add" href="/add_subject">Add New Subject</a>
        <a class="home" href="/">Home</a>

        <form method="GET" action="/subjects" style="margin-top: 20px;">
            <input type="text" name="search"
                   placeholder="Search by Subject Name or ID..."
                   value="SEARCH_VALUE">
            <button class="search-btn" type="submit">Search</button>
            <a class="reset" href="/subjects">Reset</a>
        </form>

        <table>
            <tr>
                <th>ID</th>
                <th>Subject ID</th>
                <th>Subject Name</th>
                <th>Actions</th>
            </tr>
    """

    safe_search = (search.replace("&", "&amp;")
                         .replace('"', "&quot;")
                         .replace("<", "&lt;")
                         .replace(">", "&gt;"))

    html = html.replace("SEARCH_VALUE", safe_search)

    if subjects:
        for subject in subjects:
            html += f"""
                <tr>
                    <td>{subject['id']}</td>
                    <td>{subject['subject_id']}</td>
                    <td>{subject['subject_name']}</td>
                    <td>
                        <a class="edit" href="/edit_subject/{subject['id']}">Edit</a>

                        <form action="/delete_subject/{subject['id']}"
                              method="POST" style="display:inline;"
                              onsubmit="return confirm('Delete this subject?');">
                            <button class="delete" type="submit">Delete</button>
                        </form>
                    </td>
                </tr>
            """
    else:
        html += """
            <tr>
                <td colspan="4">No subjects found!</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html



# ADD SUBJECT

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

        return """
        <h2>Subject added successfully!</h2>
        <a href="/subjects">View Subjects</a>
        <a href="/">Home</a>
        """

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Subject</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f0f4f8;
                margin: 0;
                padding: 30px;
            }

            .container {
                background: white;
                max-width: 450px;
                margin: 40px auto;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 3px 12px #cccccc;
            }

            h2 {
                text-align: center;
                color: #1e3a8a;
            }

            label {
                display: block;
                margin-top: 18px;
                font-weight: bold;
            }

            input {
                width: 100%;
                padding: 12px;
                margin-top: 7px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 6px;
            }

            button {
                width: 100%;
                background: #2563eb;
                color: white;
                padding: 13px;
                border: none;
                border-radius: 6px;
                margin-top: 25px;
                cursor: pointer;
                font-size: 16px;
            }

            button:hover {
                background: #1e40af;
            }

            .back {
                display: block;
                text-align: center;
                margin-top: 20px;
                color: #2563eb;
                text-decoration: none;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h2>Add New Subject</h2>

            <form method="POST">

                <label>Subject ID</label>
                <input type="text" name="subject_id" required>

                <label>Subject Name</label>
                <input type="text" name="subject_name" required>

                <button type="submit">Add Subject</button>

            </form>

            <a class="back" href="/">Back to Home</a>

        </div>

    </body>
    </html>
    """



# EDIT SUBJECT

@app.route("/edit_subject/<int:id>", methods=["GET", "POST"])
def edit_subject_page(id):
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

        return """
        <h2>Subject updated successfully!</h2>
        <a href="/subjects">View Subjects</a>
        <a href="/">Home</a>
        """

    subject = connection.execute(
        "SELECT * FROM subjects WHERE id = ?", (id,)
    ).fetchone()

    connection.close()

    if subject is None:
        return "Subject not found!"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Edit Subject</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f0f4f8;
                margin: 0;
                padding: 30px;
            }}

            .container {{
                background: white;
                max-width: 450px;
                margin: 40px auto;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 3px 12px #cccccc;
            }}

            h2 {{
                text-align: center;
                color: #1e3a8a;
            }}

            label {{
                display: block;
                margin-top: 18px;
                font-weight: bold;
            }}

            input {{
                width: 100%;
                padding: 12px;
                margin-top: 7px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 6px;
            }}

            button {{
                width: 100%;
                background: #2563eb;
                color: white;
                padding: 13px;
                border: none;
                border-radius: 6px;
                margin-top: 25px;
                cursor: pointer;
                font-size: 16px;
            }}

            button:hover {{
                background: #1e40af;
            }}

            .back {{
                display: block;
                text-align: center;
                margin-top: 20px;
                color: #2563eb;
                text-decoration: none;
            }}
        </style>
    </head>

    <body>
        <div class="container">

            <h2>Edit Subject Details</h2>

            <form method="POST">

                <label>Subject ID</label>
                <input type="text" name="subject_id"
                       value="{subject['subject_id']}" required>

                <label>Subject Name</label>
                <input type="text" name="subject_name"
                       value="{subject['subject_name']}" required>

                <button type="submit">Update Subject</button>

            </form>

            <a class="back" href="/subjects">Back to Subjects</a>

        </div>
    </body>
    </html>
    """



# DELETE SUBJECT
@app.route("/delete_subject/<int:id>", methods=["POST"])
def delete_subject(id):
    connection = get_db_connection()
    connection.execute("DELETE FROM subjects WHERE id = ?", (id,))
    connection.commit()
    connection.close()

    return '<p>Subject deleted successfully!</p><a href="/subjects">Back to Subjects</a>'


@app.route("/student_details/<int:id>")
def student_details(id):
    connection = get_db_connection()

    student = connection.execute(
        "SELECT * FROM students WHERE id = ?", (id,)
    ).fetchone()

    connection.close()

    if student is None:
        return "Student not found!"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Details</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f0f4f8;
                padding: 30px;
            }}

            .card {{
                background: white;
                max-width: 500px;
                margin: 40px auto;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 3px 10px #ccc;
            }}

            h1 {{
                color: #1e3a8a;
                text-align: center;
            }}

            p {{
                font-size: 17px;
                padding: 8px;
                border-bottom: 1px solid #ddd;
            }}

            a {{
                display: inline-block;
                background: #475569;
                color: white;
                padding: 10px 15px;
                text-decoration: none;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Student Details</h1>

            <p><b>Student ID:</b> {student['student_id']}</p>
            <p><b>Name:</b> {student['name']}</p>
            <p><b>Email:</b> {student['email']}</p>
            <p><b>Phone:</b> {student['phone']}</p>

            <a href="/students">Back to Students</a>
        </div>
    </body>
    </html>
    """


# RUN APPLICATION
if __name__ == "__main__":
    app.run(debug=True)

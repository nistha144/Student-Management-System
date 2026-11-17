from flask import Flask, render_template, request, session, redirect, url_for
from database import get_db_connection
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "student-academic-system-secret-key"


@app.route("/")
def home():
    return "Student Attendance System is Running!"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        connection = get_db_connection()

        existing_user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if existing_user:
            connection.close()
            return "Username already exists. Please choose another username."

        connection.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, generate_password_hash(password), role)
        )

        connection.commit()
        connection.close()

        return "Account created successfully!"

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = get_db_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        connection.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            if user["role"] == "teacher":
                return render_template("teacher_dashboard.html")

            elif user["role"] == "student":
                return render_template("student_dashboard.html")

        return "Invalid username or password!"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug=True)
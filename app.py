from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("students.db")

@app.route("/")
def index():
    db = get_db()
    students = db.execute("SELECT * FROM students").fetchall()
    db.close()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    course = request.form["course"]
    db = get_db()
    db.execute("INSERT INTO students (name, course) VALUES (?, ?)", (name, course))
    db.commit()
    db.close()
    return redirect("/")

if __name__ == "__main__":
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            course TEXT
        )
    """)
    db.commit()
    db.close()
    app.run(debug=True)

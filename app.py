from flask import Flask, render_template, request, redirect, session
from ai.quiz_generator import generate_quiz
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rasi13",
    database="ai_quiz"
)

cursor = db.cursor()

app = Flask(__name__)
app.secret_key = "secret123"

# HOME
@app.route("/")
def home():
    return render_template("landing.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form["email"]
        return redirect("/quiz")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        cursor.execute(
            "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
            (name, email, phone, password)
        )
        db.commit()

        return redirect("/login")

    return render_template("register.html")

# QUIZ
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        topic = request.form["topic"]
        difficulty = request.form["difficulty"]

        quiz = generate_quiz(topic, difficulty)

        return render_template("quiz.html", quiz=quiz, topic=topic)

    return render_template("quiz.html", quiz=None)

# ================= LEADERBOARD =================
@app.route('/leaderboard')
def leaderboard():
    cursor = db.cursor()   # 👈 add this line
    cursor.execute("SELECT * FROM leaderboard ORDER BY score DESC")
    data = cursor.fetchall()
    return render_template("leaderboard.html", data=data)

# ================= HISTORY =================
@app.route("/history")
def history():
    user = session.get("user")
    cursor.execute("SELECT * FROM history WHERE name=%s", (user,))
    data = cursor.fetchall()
    return render_template("history.html", data=data)

# RESULT
@app.route("/result", methods=["POST"])
def result():
    score = 0
    total = int(request.form["total"])

    results = []

    for i in range(total):
        selected = request.form.get(f"q{i}")
        correct = request.form.get(f"correct{i}")

        if selected == correct:
            score += 1
            status = "correct"
        else:
            status = "wrong"

        results.append({
            "question_no": i + 1,
            "selected": selected,
            "correct": correct,
            "status": status
        })

    return render_template("result.html", score=score, total=total, results=results)

# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
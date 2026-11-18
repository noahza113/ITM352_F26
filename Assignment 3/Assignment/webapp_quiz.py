"""Flask version of the Assignment 1 quiz."""

import json
import os
import random
import time
from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(
    __name__,
    template_folder=str(Path(__file__).parent),
    static_folder=str(Path(__file__).parent / "static"),
)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(32))

DATA_FOLDER = Path(__file__).parent / "data"
QUESTIONS_FILE = DATA_FOLDER / "questions.json"
USERS_FILE = DATA_FOLDER / "users.json"
SCORES_FILE = DATA_FOLDER / "scores.json"
QUESTIONS_PER_QUIZ = 5


def load_questions():
    """Read questions from the JSON file and put them in a simple list."""
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        question_data = json.load(file)

    questions = []
    for category in question_data:
        for question_name in question_data[category]:
            details = question_data[category][question_name]

            if question_name == "double_or_nothing":
                question_text = details["question"]
            else:
                question_text = question_name

            questions.append(
                {
                    "category": category,
                    "question": question_text,
                    "answers": details["answers"],
                    "hint": details["hint"],
                }
            )

    return questions


def read_json_file(file_path, empty_value):
    """Read a JSON file, or return an empty value if it does not exist yet."""
    if not file_path.exists():
        return empty_value

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json_file(file_path, data):
    """Save data in a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def show_home(error=None):
    """Show the home page and the current user's recent scores."""
    questions = load_questions()
    scores = read_json_file(SCORES_FILE, [])
    user_scores = [
        score for score in scores
        if score["username"] == session.get("username")
    ]
    return render_template(
        "index.html",
        username=session.get("username"),
        categories=sorted({question["category"] for question in questions}),
        question_count=len(questions),
        scores=user_scores[-5:][::-1],
        error=error,
    )


def save_quiz_score(quiz):
    """Add the finished quiz to the JSON score file."""
    scores = read_json_file(SCORES_FILE, [])
    scores.append(
        {
            "username": session["username"],
            "score": quiz["score"],
            "total": len(quiz["questions"]),
            "time_taken": quiz["time_taken"],
            "category_scores": quiz["category_scores"],
        }
    )
    save_json_file(SCORES_FILE, scores)


@app.route("/")
def index():
    try:
        return show_home()
    except (OSError, json.JSONDecodeError, KeyError) as error:
        app.logger.error("Could not load quiz data: %s", error)
        return render_template(
            "index.html",
            username=session.get("username"),
            categories=[],
            question_count=0,
            scores=[],
            error="The quiz data could not be loaded. Check the JSON files in the data folder.",
        ), 500


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", "").strip().lower()
    password = request.form.get("password", "")

    if not username.isalnum() or len(username) < 3 or len(username) > 20:
        return show_home("Username must be 3 to 20 letters or numbers.")
    if len(password) < 8:
        return show_home("Password must have at least 8 characters.")

    try:
        users = read_json_file(USERS_FILE, {})
        if username in users:
            return show_home("That username is already registered.")

        # Save a password hash instead of saving the password itself.
        users[username] = generate_password_hash(password)
        save_json_file(USERS_FILE, users)
    except (OSError, json.JSONDecodeError) as error:
        app.logger.error("Could not register user: %s", error)
        return show_home("Account data could not be saved.")

    session.clear()
    session["username"] = username
    return redirect(url_for("index"))


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip().lower()
    password = request.form.get("password", "")

    if not username or not password:
        return show_home("Enter both your username and password.")

    try:
        users = read_json_file(USERS_FILE, {})
    except (OSError, json.JSONDecodeError) as error:
        app.logger.error("Could not read account data: %s", error)
        return show_home("Account data could not be loaded.")

    if username not in users or not check_password_hash(users[username], password):
        return show_home("Username or password is incorrect.")

    session.clear()
    session["username"] = username
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/start", methods=["POST"])
def start_quiz():
    if "username" not in session:
        return redirect(url_for("index"))

    category = request.form.get("category")
    try:
        questions = load_questions()
    except (OSError, json.JSONDecodeError, KeyError) as error:
        app.logger.error("Could not load question data: %s", error)
        return render_template(
            "index.html",
            username=session.get("username"),
            categories=[],
            question_count=0,
            scores=[],
            error="The question data could not be loaded.",
        )
    available_categories = {question["category"] for question in questions}

    if category == "all":
        chosen_questions = questions
    elif category in available_categories:
        chosen_questions = [
            question for question in questions if question["category"] == category
        ]
    else:
        return show_home("Please choose a valid category.")

    quiz_questions = random.sample(
        chosen_questions,
        min(QUESTIONS_PER_QUIZ, len(chosen_questions)),
    )

    session["quiz"] = {
        "questions": quiz_questions,
        "question_number": 0,
        "score": 0,
        "answers": [],
        "start_time": time.time(),
        "feedback": None,
    }
    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "username" not in session or "quiz" not in session:
        return redirect(url_for("index"))

    quiz_data = session["quiz"]
    question_number = quiz_data["question_number"]
    questions = quiz_data["questions"]

    if question_number >= len(questions):
        return redirect(url_for("result"))

    question = questions[question_number]

    if "options" not in quiz_data:
        options = question["answers"].copy()
        random.shuffle(options)
        quiz_data["options"] = options
        session["quiz"] = quiz_data

    if request.method == "POST":
        action = request.form.get("action")

        if action == "answer" and quiz_data.get("answered"):
            return redirect(url_for("quiz"))

        if action == "answer":
            answer = request.form.get("answer", "")
            options = quiz_data["options"]

            if not answer.isdigit() or int(answer) >= len(options):
                return render_template(
                    "quiz.html",
                    question=question,
                    question_number=question_number + 1,
                    total_questions=len(questions),
                    options=options,
                    feedback=quiz_data.get("feedback"),
                    feedback_correct=quiz_data.get("feedback_correct"),
                    error="Please choose one of the answers.",
                    answered=False,
                    hint=question["hint"],
                    hint_shown=False,
                )

            selected_answer = options[int(answer)]
            correct_answer = question["answers"][0]
            is_correct = selected_answer == correct_answer

            if is_correct:
                quiz_data["score"] += 1
                feedback = "Correct!"
            else:
                feedback = "Incorrect. The correct answer was " + correct_answer + "."

            quiz_data["answers"].append(
                {
                    "category": question["category"],
                    "question": question["question"],
                    "your_answer": selected_answer,
                    "correct_answer": correct_answer,
                    "correct": is_correct,
                }
            )
            quiz_data["feedback"] = feedback
            quiz_data["feedback_correct"] = is_correct
            quiz_data["answered"] = True
            session["quiz"] = quiz_data

        elif action == "next" and quiz_data.get("answered"):
            quiz_data["question_number"] += 1
            quiz_data.pop("options", None)
            quiz_data.pop("answered", None)
            quiz_data["feedback"] = None
            quiz_data.pop("feedback_correct", None)

            if quiz_data["question_number"] == len(questions):
                quiz_data["time_taken"] = int(time.time() - quiz_data["start_time"])
                quiz_data["category_scores"] = {}
                for answer in quiz_data["answers"]:
                    category = answer["category"]
                    if category not in quiz_data["category_scores"]:
                        quiz_data["category_scores"][category] = {
                            "correct": 0,
                            "total": 0,
                        }
                    quiz_data["category_scores"][category]["total"] += 1
                    if answer["correct"]:
                        quiz_data["category_scores"][category]["correct"] += 1

                try:
                    save_quiz_score(quiz_data)
                except (OSError, json.JSONDecodeError) as error:
                    app.logger.error("Could not save quiz score: %s", error)
                    return render_template(
                        "quiz.html",
                        question=question,
                        question_number=question_number + 1,
                        total_questions=len(questions),
                        options=quiz_data["options"],
                        feedback=quiz_data.get("feedback"),
                        feedback_correct=quiz_data.get("feedback_correct"),
                        error="Your score could not be saved. Please try again.",
                        answered=True,
                        hint=question["hint"],
                        hint_shown=False,
                    )
                session.pop("quiz")
                session["result"] = quiz_data
                return redirect(url_for("result"))

            session["quiz"] = quiz_data
            return redirect(url_for("quiz"))

    return render_template(
        "quiz.html",
        question=question,
        question_number=question_number + 1,
        total_questions=len(questions),
        options=quiz_data["options"],
        feedback=quiz_data.get("feedback"),
        feedback_correct=quiz_data.get("feedback_correct"),
        error=None,
        hint=question["hint"],
        answered=quiz_data.get("answered", False),
        hint_shown=request.form.get("action") == "hint",
    )


@app.route("/result")
def result():
    if "username" not in session or "result" not in session:
        return redirect(url_for("index"))

    quiz_data = session["result"]
    incorrect_answers = [
        answer for answer in quiz_data["answers"] if not answer["correct"]
    ]
    improvement_areas = {}
    for answer in incorrect_answers:
        category = answer["category"]
        if category not in improvement_areas:
            improvement_areas[category] = 0
        improvement_areas[category] += 1

    return render_template(
        "Result.html",
        score=quiz_data["score"],
        total_questions=len(quiz_data["questions"]),
        correct_count=quiz_data["score"],
        incorrect_count=len(incorrect_answers),
        time_taken=quiz_data["time_taken"],
        category_scores=quiz_data["category_scores"],
        improvement_areas=improvement_areas,
        incorrect_answers=incorrect_answers,
    )


if __name__ == "__main__":
    app.run(debug=True)

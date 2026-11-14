import json
import os
import random
from pathlib import Path
from string import ascii_lowercase

from flask import Flask, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(32))

QUESTIONS_PATH = (
    Path(__file__).resolve().parents[1]
    / "Assignment 1"
    / "Assignment"
    / "questions.json"
)
NUM_QUESTIONS_PER_QUIZ = 5

with QUESTIONS_PATH.open("r", encoding="utf-8") as questions_file:
    QUESTIONS = json.load(questions_file)

PAGE_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ title }} - Assignment 1 Quiz</title>
    <style>
        body {
            background: #f3f6fa;
            color: #172033;
            font: 1rem/1.5 system-ui, sans-serif;
            margin: 0;
        }
        main {
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 24px #17203318;
            margin: 4rem auto;
            max-width: 42rem;
            padding: 2rem;
            width: calc(100% - 4rem);
        }
        h1 { margin-top: 0; }
        fieldset { border: 0; margin: 1.5rem 0; padding: 0; }
        label { display: block; margin: 0.6rem 0; }
        button, select {
            border: 1px solid #53627a;
            border-radius: 6px;
            font: inherit;
            padding: 0.55rem 0.8rem;
        }
        button {
            background: #174ea6;
            border-color: #174ea6;
            color: white;
            cursor: pointer;
        }
        button:hover { background: #103c82; }
        .secondary { background: white; color: #174ea6; }
        .notice { background: #eef4ff; border-radius: 6px; padding: 0.8rem; }
        .error { color: #a32121; }
        .muted { color: #53627a; }
    </style>
</head>
<body>
<main>
    <h1>Assignment 1 Quiz</h1>
    {% if page == "home" %}
        <p>Choose a category to start a five-question quiz.</p>
        {% if error %}<p class="error" role="alert">{{ error }}</p>{% endif %}
        <form action="{{ url_for('start_quiz') }}" method="post">
            <label for="category">Category</label>
            <select id="category" name="category" required>
                {% for category in categories %}
                    <option value="{{ category }}">{{ category }}</option>
                {% endfor %}
            </select>
            <p><button type="submit">Start quiz</button></p>
        </form>
    {% elif page == "question" %}
        <p class="muted">{{ category }} · Question {{ question_number }} of {{ total_questions }}</p>
        {% if feedback %}<p class="notice" role="status">{{ feedback }}</p>{% endif %}
        <h2>{{ question }}</h2>
        <form action="{{ url_for('quiz') }}" method="post">
            <fieldset>
                <legend>Choose an answer</legend>
                {% for label, answer in options %}
                    <label>
                        <input type="radio" name="answer" value="{{ label }}" required>
                        {{ label }}. {{ answer }}
                    </label>
                {% endfor %}
            </fieldset>
            {% if hint_shown %}<p class="notice">Hint: {{ hint }}</p>{% endif %}
            {% if error %}<p class="error" role="alert">{{ error }}</p>{% endif %}
            <button type="submit" name="action" value="answer">Submit answer</button>
            <button class="secondary" type="submit" name="action" value="hint">Show hint</button>
        </form>
    {% elif page == "bonus_offer" %}
        <p class="notice">You scored {{ score }} point(s). A correct bonus answer doubles your score; an incorrect answer loses it all.</p>
        <form action="{{ url_for('bonus') }}" method="post">
            <button type="submit" name="action" value="yes">Play double or nothing</button>
            <button class="secondary" type="submit" name="action" value="no">Keep my score</button>
        </form>
    {% elif page == "bonus_question" %}
        <p class="muted">Double or nothing</p>
        <h2>{{ question }}</h2>
        <form action="{{ url_for('bonus') }}" method="post">
            <fieldset>
                <legend>Choose an answer</legend>
                {% for label, answer in options %}
                    <label>
                        <input type="radio" name="answer" value="{{ label }}" required>
                        {{ label }}. {{ answer }}
                    </label>
                {% endfor %}
            </fieldset>
            {% if hint_shown %}<p class="notice">Hint: {{ hint }}</p>{% endif %}
            {% if error %}<p class="error" role="alert">{{ error }}</p>{% endif %}
            <button type="submit" name="action" value="answer">Submit answer</button>
            <button class="secondary" type="submit" name="action" value="hint">Show hint</button>
        </form>
    {% elif page == "result" %}
        <h2>Quiz complete</h2>
        {% if feedback %}<p class="notice" role="status">{{ feedback }}</p>{% endif %}
        <p>Your final score: <strong>{{ score }} point(s)</strong>.</p>
        <a href="{{ url_for('index') }}">Play again</a>
    {% endif %}
</main>
</body>
</html>
"""


def render_page(title, **context):
    return render_template_string(PAGE_TEMPLATE, title=title, **context)


def current_options(question_data):
    answers = question_data["answers"]
    labels = ascii_lowercase[: len(answers)]
    return list(zip(labels, random.sample(answers, k=len(answers))))


@app.route("/")
def index():
    return render_page("Choose a category", page="home", categories=QUESTIONS.keys())


@app.route("/start", methods=["POST"])
def start_quiz():
    category = request.form.get("category")
    if category not in QUESTIONS:
        return render_page(
            "Choose a category",
            page="home",
            categories=QUESTIONS.keys(),
            error="Please choose a valid category.",
        ), 400

    category_data = QUESTIONS[category]
    question_names = [
        name for name in category_data if name != "double_or_nothing"
    ]
    session.clear()
    session.update(
        category=category,
        question_names=random.sample(
            question_names, k=min(NUM_QUESTIONS_PER_QUIZ, len(question_names))
        ),
        question_index=0,
        score=0,
        stage="question",
        hint_shown=False,
        feedback=None,
    )
    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    stage = session.get("stage")
    if stage == "bonus_offer":
        return redirect(url_for("bonus"))
    if stage == "result":
        return redirect(url_for("result"))
    if stage != "question":
        return redirect(url_for("index"))

    question_names = session["question_names"]
    question_index = session["question_index"]
    category_data = QUESTIONS[session["category"]]
    question_name = question_names[question_index]
    question_data = category_data[question_name]
    options = session.get("options")

    if not options:
        options = current_options(question_data)
        session["options"] = options

    error = None
    if request.method == "POST":
        action = request.form.get("action")
        if action == "hint":
            session["hint_shown"] = True
            return redirect(url_for("quiz"))
        if action != "answer":
            error = "Please submit an answer or request a hint."
        else:
            answer_label = request.form.get("answer")
            answer_by_label = dict(options)
            if answer_label not in answer_by_label:
                error = "Please select one of the listed answers."
            elif answer_by_label[answer_label] == question_data["answers"][0]:
                session["score"] += 1
                session["feedback"] = "Correct!"
            else:
                session["feedback"] = (
                    f"Incorrect. The correct answer was {question_data['answers'][0]}."
                )

            if not error:
                session["question_index"] += 1
                session["hint_shown"] = False
                session.pop("options", None)
                if session["question_index"] == len(question_names):
                    if session["score"] > 0:
                        session["stage"] = "bonus_offer"
                    else:
                        session["stage"] = "result"
                return redirect(url_for("quiz"))

    if session["stage"] == "result":
        return redirect(url_for("result"))
    if session["stage"] == "bonus_offer":
        return redirect(url_for("bonus"))

    return render_page(
        "Question",
        page="question",
        category=session["category"],
        question_number=question_index + 1,
        total_questions=len(question_names),
        question=question_name,
        options=options,
        hint=question_data["hint"],
        hint_shown=session.get("hint_shown", False),
        feedback=session.pop("feedback", None),
        error=error,
    )


@app.route("/bonus", methods=["GET", "POST"])
def bonus():
    stage = session.get("stage")
    if stage not in ("bonus_offer", "bonus_question"):
        return redirect(url_for("index"))

    if request.method == "POST":
        action = request.form.get("action")
        if stage == "bonus_offer":
            if action == "no":
                session["stage"] = "result"
                return redirect(url_for("result"))
            if action == "yes":
                session["stage"] = "bonus_question"
                session["hint_shown"] = False
                session.pop("options", None)
                return redirect(url_for("bonus"))
        elif action == "hint":
            session["hint_shown"] = True
            return redirect(url_for("bonus"))
        elif action == "answer":
            bonus_data = QUESTIONS[session["category"]]["double_or_nothing"]
            options = session.get("options") or current_options(bonus_data)
            answer_by_label = dict(options)
            answer_label = request.form.get("answer")
            if answer_label in answer_by_label:
                if answer_by_label[answer_label] == bonus_data["answers"][0]:
                    session["score"] *= 2
                    session["feedback"] = "Correct! Your points are doubled."
                else:
                    session["score"] = 0
                    session["feedback"] = (
                        f"Incorrect. The correct answer was {bonus_data['answers'][0]}."
                    )
                session["stage"] = "result"
                return redirect(url_for("result"))

    if stage == "bonus_offer":
        return render_page(
            "Double or nothing", page="bonus_offer", score=session["score"]
        )

    bonus_data = QUESTIONS[session["category"]]["double_or_nothing"]
    options = session.get("options")
    if not options:
        options = current_options(bonus_data)
        session["options"] = options
    return render_page(
        "Bonus question",
        page="bonus_question",
        question=bonus_data["question"],
        options=options,
        hint=bonus_data["hint"],
        hint_shown=session.get("hint_shown", False),
        error=(
            "Please select one of the listed answers."
            if request.method == "POST"
            else None
        ),
    )


@app.route("/result")
def result():
    if session.get("stage") != "result":
        return redirect(url_for("index"))
    return render_page(
        "Results",
        page="result",
        score=session["score"],
        feedback=session.pop("feedback", None),
    )


if __name__ == "__main__":
    app.run()
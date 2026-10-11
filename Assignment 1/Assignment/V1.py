import json
import random
from pathlib import Path
from string import ascii_lowercase

questions_path = Path(__file__).resolve().with_name("questions.json")

with questions_path.open("r", encoding="utf-8") as file:
    questions = json.load(file)

NUM_QUESTIONS_PER_QUIZ = 5

categories = list(questions)
print("Choose a category:")
for category_num, category in enumerate(categories, start=1):
    print(f"{category_num}. {category}")

while True:
    category_choice = input("Category number? ").strip()
    if category_choice.isdigit() and 1 <= int(category_choice) <= len(categories):
        selected_category = categories[int(category_choice) - 1]
        break
    print(f"Please enter a number from 1 to {len(categories)}.")

category_data = questions[selected_category]
category_questions = {
    question: question_data
    for question, question_data in category_data.items()
    if question != "double_or_nothing"
}
num_questions = min(NUM_QUESTIONS_PER_QUIZ, len(category_questions))
selected_questions = random.sample(list(category_questions.items()), k=num_questions)

num_correct = 0

for num, (question, question_data) in enumerate(selected_questions, start=1):
    answers = question_data["answers"]
    hint = question_data["hint"]
    correct_answer = answers[0]
    print(f"\nQuestion {num}: {question}")

    sorted_answers = sorted(answers)
    labeled_answers = dict(zip(ascii_lowercase, random.sample(sorted_answers, k=len(sorted_answers))))

    for label, answer in labeled_answers.items():
        print(f"{label}. {answer}")
        
    while True:
        answer_label = input("Choice (or ? for a hint)? ").strip().lower()
        if answer_label == "?":
            print(f"Hint: {hint}")
            continue
        if answer_label in labeled_answers:
            break
        print(f"Invalid choice. Please select one of {', '.join(labeled_answers.keys())}, or ? for a hint.")

    answer = labeled_answers.get(answer_label)

    if answer == correct_answer:
        print("Correct!")
        num_correct += 1
    else:
        print(f"The answer is '{correct_answer!r}', not {answer!r}.")

print(f"\nYou got {num_correct} out of {len(selected_questions)} correct.")

final_score = num_correct
if final_score > 0:
    while True:
        gamble_choice = input(
            f"You have {final_score} point(s). Double or nothing? (yes/no) "
        ).strip().lower()
        if gamble_choice in ("yes", "y", "no", "n"):
            break
        print("Please enter yes or no.")

    if gamble_choice in ("yes", "y"):
        bonus_question = category_data["double_or_nothing"]
        question = bonus_question["question"]
        answers = bonus_question["answers"]
        correct_answer = answers[0]
        print(f"\nDouble-or-nothing question: {question}")

        labeled_answers = dict(zip(
            ascii_lowercase,
            random.sample(answers, k=len(answers)),
        ))
        for label, answer in labeled_answers.items():
            print(f"{label}. {answer}")

        while True:
            answer_label = input("Choice (or ? for a hint)? ").strip().lower()
            if answer_label == "?":
                print(f"Hint: {bonus_question['hint']}")
                continue
            if answer_label in labeled_answers:
                break
            print(
                f"Invalid choice. Please select one of "
                f"{', '.join(labeled_answers.keys())}, or ? for a hint."
            )

        if labeled_answers[answer_label] == correct_answer:
            final_score *= 2
            print("Correct! Your points are doubled.")
        else:
            final_score = 0
            print(f"Incorrect. The correct answer was {correct_answer!r}. You lose your points.")
else:
    print("You need at least one point to play double or nothing.")

print(f"Final score: {final_score} point(s).")
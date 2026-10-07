#Interactive quiz system; second version
#Make a dictionary with the questions and answers
# Allow the user to choose the option by it's label'
# Improve the look and visability. Keep track of correct answers.
#Randomize the order of the answers and the questions.
from string import ascii_lowercase
import random

questions = {
    "What is the capital of France?": ["Paris", "Toulouse", "Nice", "Avignon", "Lyon", "Marseille"],
    "What is the capital of Germany?": ["Berlin", "Munich", "Hamburg", "Frankfurt"],
    "What is the capital of Italy?": ["Rome", "Florence", "Venice", "Milan", "Naples", "Turin"]
    "The Last Supper was painted by which artist?": ["Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"],
}

NUM_QUESTIONS_PER_QUIZ = 5

num_question = (min(NUM_QUESTIONS_PER_QUIZ, len(questions)))
selected_questions = random.sample(list(questions.items()), num_question)

num_correct = 0

for num, (question, answers) in enumerate(selected_questions, start=1):
    correct_answer = answers[0]
    print(f"Question {num}: {question}")

    
    sorted_answers = sorted(answers)
    labeled_answers = dict(zip(ascii_lowercase, (sorted_answers,k=len(sorted_answers))))

    for label, answer in labeled_answers.items():
        print(f"{label}. {answer}")

    while (answer_label) := input("Choice? ").lower() not in labeled_answers:
        print(f"Invalid choice. Please select one of ({', '.join(labeled_answers.keys())})")
        

    answer_label = input("Choice? ").lower()
    answer = labeled_answers.get(answer_label)
    
    if answer == correct_answer:
        print("Correct!")
        num_correct += 1
    else:
        print(f"The answer is '{correct_answer}', not '{answer}' ")
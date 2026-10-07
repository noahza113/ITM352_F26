#Interactive quiz system; second version
#Make a dictionary with the questions and answers
# Allow the user to choose the option by it's label'
# Improve the look and visability. Keep track of correct answers.

questions = {
    "What is the capital of France?": ["Paris", "Toulouse", "Nice", "Avignon", "Lyon", "Marseille"],
    "What is the capital of Germany?": ["Berlin", "Munich", "Hamburg", "Frankfurt"],
    "What is the capital of Italy?": ["Rome", "Florence", "Venice", "Milan", "Naples", "Turin"]
    "The Last Supper was painted by which artist?": ["Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"],

}

correct_count = 0

for num, (question, answers) in enumerate(questions.items(),start=1):
    correct_answer = answers[0]
    sorted_answers = sorted(answers)

    for label, answer in labeled_answers.items():
        print(f"{label}. {answer}")
   
    answer_label = input("Choice? ").lower
    answer = labeled_answers.get(answer_label)
    
    if answer == correct_answer:
        print("Correct!")
        num_correct += 1
    else:
        print(f"The answer is '{correct_answer}', not '{answer}' ")
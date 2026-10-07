#Interactive quiz system; second version
#Make a dictionary with the questions and answers
# Allow the user to choose the option by it's label

questions = {
    "What is the capital of France?": ["Paris", "Toulouse", "Nice", "Avignon", "Lyon", "Marseille"],
    "What is the capital of Germany?": ["Berlin", "Munich", "Hamburg", "Frankfurt"],
    "What is the capital of Italy?": ["Rome", "Florence", "Venice", "Milan", "Naples", "Turin"]
}

for question, answers in questions.items():
    correct_answer = answers[0]
    sorted_answers = sorted(answers)

    for label, answer in enumerate(sorted_answers, start=1):
        print(f"{label}. {answer}")
   
    answer_label = input(f"{question} ")
    answer = sorted_answers[(answer_label) - 1]
    
    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The answer is '{correct_answer}', not '{answer}' ")
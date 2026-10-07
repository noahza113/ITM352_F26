#Interactive quiz system; second version
#Make a dictionary with the questions and answers

questions = {
    "What is the capital of France?": ["Paris", "Toulouse", "Nice", "Avignon", "Lyon", "Marseille"],
    "What is the capital of Germany?": ["Berlin", "Munich", "Hamburg", "Frankfurt"],
    "What is the capital of Italy?": ["Rome", "Florence", "Venice", "Milan", "Naples", "Turin"]
}

for question, answers in questions.items():
    correct_answer = answers[0]
    for answer in answers:
        print(f"- {answer}")
    answer = input(f"{question} ")
    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The answer is '{correct_answer}', not '{answer}' ")
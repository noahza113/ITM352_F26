import json

filename="quiz_quesitons.json"
with open(filename,'r') as file:
    questions = json.load(file)

print(questions)
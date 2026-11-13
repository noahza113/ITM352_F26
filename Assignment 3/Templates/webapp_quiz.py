#Application to manage the quiz webapp
#Name: Noah Zane
#Date: 11/13/2026

from flask import Flask, app, render_template, request, redirect, url_for

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    global score, question_number, max_questions, questions

    if request.method == 'POST':
        # Capture the answer from the form
        answer = request.form.get('answer')

        # Check if the answer is correct
        if answer == questions[question_number]['answer']:
            score += 1
        question_number += 1

    if question_number < max_questions:
        # Render the next question
        return render_template('quiz.html',
                               question=questions[question_number]['question'],
                               options=questions[question_number]['options'],
                                question_number=[question_number]['options'])
    else:
        # Quiz is over, display the score
        return render_template('result.html', score=score, max_questions=max_questions)

@app.route('/result')
def result():
    # Display the final score
    global score, max_questions
    return render_template('result.html', score=score, max_questions=max_questions)

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
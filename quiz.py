# Здесь будет код веб-приложения
import os
from random import shuffle
from flask import url_for, redirect, session, Flask, session, render_template, request
from db_scripts import get_question_after, get_quizes, check_answer

def start_quiz(quiz_id):
    session["quiz"] = quiz_id
    session["last_question"] = 0
    session["total"] = 0
    session["correct"] = 0

def quiz_form():
    q_list = get_quizes()
    return render_template('start.html', q_list = q_list)

def index():
    if request.method == 'GET':
        start_quiz(-1)
        print('am')
        return quiz_form()
    else:
        quiz_id = request.form.get('quiz')
        start_quiz(quiz_id)
        print('amo')
        return redirect(url_for('test'))

def save_answers():
    answer = request.form.get('ans_text')
    qu_id = request.form.get('q_id')
    session['last_question'] = qu_id
    session['total']+=1
    if check_answer(qu_id, answer):
        session['correct']+=1

def question_form(question):
    answer_list = [question[2], question[3], question[4], question[5]]
    shuffle(answer_list)
    return render_template('test.html', question = question[1], quiz_id = question[0],answers_list = answer_list)

def test():
    print('a')
    if not ('quiz' in session) or int(session['quiz'])<0:
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            save_answers()
        next_question = get_question_after(session['last_question'], session['quiz'])
        if next_question is None or len(next_question) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(next_question)

def end_quiz():
    session.clear()

def result():
    html = render_template('result.html', right = session['correct'], total = session['total'])
    end_quiz()
    return html

folder = os.getcwd()

app = Flask(__name__, template_folder=folder, static_folder=folder)
app.add_url_rule('/', 'index', index, methods =['post', 'get'])
app.add_url_rule('/test', 'test', test, methods =['post', 'get'])
app.add_url_rule('/result', 'result', result)
app.config['SECRET_KEY'] = 'MOMGOBB'
if __name__ == '__main__':
    app.run()

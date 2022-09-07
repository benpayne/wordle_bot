import re
from database import get_results, get_all, delete_result
from sim import get_first_word_stats, get_first_words
from flask import Flask, render_template, url_for, redirect
from markupsafe import escape
from datetime import date
import os
import dateutil.parser as parser 

app = Flask(__name__)
app.config.from_pyfile('config.py')

from . import game_info

@app.route("/")
def top():
    return redirect(url_for("db_info"))

@app.route("/data/db-info")
def db_info():
    data = get_all()
    steps = {}
    for d, r in data.items():
        steps[d] = len(r)
    return render_template('db_info.html', data=steps)

@app.route("/data/<date>")
def dates_pattern_json(date):
    data = None
    try:
        d = parser.isoparse(date)
        res_string, data, word_lists = get_results(d.isoformat().split("T")[0])
    except Exception as e:
        print(e)
        print(f"bad date {date}")
    print(data, word_lists)
    show_answer=False
    if data == None:
        data = [[' no  ', ['column', 'present', 'present', 'column', 'column']],['data ', ['present', 'present', 'present', 'present', 'column']]]
        show_answer=True

    rows = []
    for r in data:
        word = r[0]
        results = r[1]
        items = []
        for i, c in enumerate(results):
            items.append({'letter': word[i], 'state': c})
        rows.append({'letters': items})
    return {'res': 'OK', 'rows': rows, 'share_text': res_string, 'word_info': word_lists}


@app.route("/data/first_word/<list_name>")
def get_first_word_list(list_name):
    if list_name != 'all' and list_name != 'answers':
        return {'res': 'Bad List'}

    words = get_first_words(list_name, 20)
    word_list = []
    i = 1
    for k, v in words.items():
        word_list.append({'position': i, 'word': k, 'exp_info': v['exp_info'], 'word_weight': v['word_weight']})
        i+=1

    return {'res': 'OK', 'words': word_list}

@app.route("/data/first_word/<list_name>/<word>")
def get_first_word_data(list_name, word):
    if list_name != 'all' and list_name != 'answers':
        return {'res': 'Bad List'}

    i, v = get_first_word_stats(list_name, word)

    return {'res': 'OK', 'words': [{'position': i, 'word': word, 'exp_info': v['exp_info'], 'word_weight': v['word_weight']}]}

@app.route("/delete/<date>")
def delete_date(date):
    try:
        d = parser.isoparse(date)
        res_string, data = delete_result(d.isoformat().split("T")[0])
    except:
        print(f"bad date {date}")
    return redirect(url_for("top"))

    
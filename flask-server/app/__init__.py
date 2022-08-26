import re
from database import get_results, get_all, delete_result
from flask import Flask, render_template, url_for, redirect
from markupsafe import escape
from datetime import date
import os
import dateutil.parser as parser 

class Config:
    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            "id": "startup",
            "func": "app.jobs:startup_test",
            "trigger": "date",
        }
    ]

app = Flask(__name__)
app.config.from_object(Config())
app.config.from_pyfile('config.py')

from . import game_info

@app.route("/")
def top():
    return render_template('top.html')

@app.route("/db-info")
def db_info():
    global addr, port
    data = get_all()
    steps = {}
    for d, r in data.items():
        steps[d] = len(r)
    return render_template('db_info.html', data=steps, selenium_addr=addr, selenium_port=port)

@app.route("/pattern/<date>")
def dates_pattern(date):
    data = None
    try:
        d = parser.isoparse(date)
        res_string, data = get_results(d.isoformat().split("T")[0])
    except:
        print(f"bad date {date}")
    print(data)
    show_answer=False
    if data == None:
        data = [[' no  ', ['column', 'present', 'present', 'column', 'column']],['data ', ['present', 'present', 'present', 'present', 'column']]]
        show_answer=True
    return render_template('answer.html', result="", data=data, date=date, show_answer=show_answer)


@app.route("/data/<date>")
def dates_pattern_json(date):
    data = None
    try:
        d = parser.isoparse(date)
        res_string, data = get_results(d.isoformat().split("T")[0])
    except:
        print(f"bad date {date}")
    print(data)
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
    return {'res': 'OK', 'rows': rows}



@app.route("/answer/<date>")
def dates_answer(date):
    data = None
    try:
        d = parser.isoparse(date)
        res_string, data = get_results(d.isoformat().split("T")[0])
    except:
        print(f"bad date {date}")
    print(data)
    return render_template('answer.html', result="", data=data, date=date, show_answer=True)


@app.route("/delete/<date>")
def delete_date(date):
    try:
        d = parser.isoparse(date)
        res_string, data = delete_result(d.isoformat().split("T")[0])
    except:
        print(f"bad date {date}")
    return redirect(url_for("top"))


@app.route("/play")
def play_wordle():
    return render_template('play.html')
    
from database import get_results, get_all, delete_result
from play import wordle_bot
from flask import Flask, render_template, url_for, redirect
from markupsafe import escape
from datetime import date
import os
import dateutil.parser as parser 

addr = os.getenv("SELENIUM_ADDR")
port = os.getenv("SELENIUM_PORT")
if addr == None:
    addr = "192.168.1.202"
if port == None:
    port = 31496

class Config:
    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            "id": "startup",
            "func": "app.jobs:startup_test",
            "trigger": "date",
        }
    ]

print(f"Selenium addr:port {addr}:{port}")

app = Flask(__name__)
app.config.from_object(Config())


from . import jobs

@app.route("/")
def top():
    return render_template('top.html')

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
    
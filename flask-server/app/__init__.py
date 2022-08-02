from database import get_results
from play import wordle_bot
from flask import Flask, render_template, url_for
from markupsafe import escape
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(wordle_bot, trigger='cron', hour='0', minute='20')
scheduler.start()

if get_results(date.today().isoformat()):
    scheduler.add_job(wordle_bot)

app = Flask(__name__)

@app.route("/")
def top_page():
    res_string, data = get_results(date.today().isoformat())
    return render_template('top.html', result="", data=data, show_answer=False)

@app.route("/answer")
def todays_answer():
    res_string, data = get_results(date.today().isoformat())
    return render_template('top.html', result="", data=data, show_answer=True)

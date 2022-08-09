from flask_apscheduler import APScheduler
from database import get_results, get_all
from . import app, addr, port
from play import wordle_bot
from datetime import date
from flask import Flask, render_template, url_for, redirect

def startup_test():
    print("Checking for todays data in DB")
    res = get_results(date.today().isoformat())
    print(f"got {res}")
    if res[0] == None:
        print("Running wordle_bot")
        wordle_bot(addr, port, False)
        print("Complete")

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

scheduler.add_job("startup", startup_test, replace_existing=True)
print("Start job scheduled")

@scheduler.task('cron', id='daily_job', hour='0', minute='20')
def daily_refresh():
    wordle_bot(addr, port, False)

@app.route("/db-info")
def db_info():
    global addr, port
    data = get_all()
    steps = {}
    for d, r in data.items():
        steps[d] = len(r)
    print(scheduler.get_jobs())
    return render_template('db_info.html', data=steps, selenium_addr=addr, selenium_port=port, jobs=scheduler.get_jobs())


@app.route("/load-data")
def load_data():
    global addr, port
    print("Trigger loading todays data")
    scheduler.add_job(id="web-load", func=wordle_bot, args=[addr, port, False])
    return redirect(url_for("db_info"))


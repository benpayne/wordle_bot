from email.contentmanager import raw_data_manager
import os
import sqlalchemy as db
from sqlalchemy import create_engine, select, Column, Integer, String, PrimaryKeyConstraint, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from datetime import date
import json
import threading
import queue

base_dir = os.path.dirname(os.path.abspath(__file__))
#DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'database.sqlite3')
DATABASE_URI = os.getenv("DATABASE_URI")
if DATABASE_URI == None:
    DATABASE_URI = 'mysql://wordle-readonly:abc123@35.224.199.116/wordle'

Base = declarative_base()
class Results(Base):
    __tablename__ = "results_data"
    __table_args__ = (
        PrimaryKeyConstraint('date'),
    )
    date = Column(String(60), primary_key=True)
    result_string = Column(String(1000))
    row_data = Column(String(1000))
    word_data = Column(JSON)

db_thread = None
db_event = None
db_resoponse = None

def db_thread_main():
    global db_thread
    global db_event, db_resoponse
    print(f"DATABASE_URI = {DATABASE_URI}")
    engine = create_engine(DATABASE_URI)
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)

    print("Thread started")
    ev = db_event.get()
    while ev:
        print(f"Got event {ev[0]}")
        if ev[0] == "quit":
            return
        elif ev[0] == "store":
            s = session()
            r = s.query(Results).filter_by(date=date.today().isoformat()).first()
            if r:
                s.delete(r)
            r = Results(date=date.today().isoformat(), result_string=ev[1], row_data=ev[2], word_data=ev[3])
            s.add(r)
            s.commit()
            s.close()
        elif ev[0] == "get":
            s = session()
            print(f"getting data for {ev[1]}")
            try:
                r = s.query(Results).filter_by(date=ev[1]).first()
                print(r.date)
                db_resoponse.put((json.loads(r.result_string), json.loads(r.row_data), json.loads(r.word_data)))
            except:
                db_resoponse.put((None, None, None))
            s.close()
        elif ev[0] == "get-all":
            s = session()
            try:
                r = s.query(Results).all()
                print(r)
                all_data = {}
                for row in r:
                    all_data[row.date] = json.loads(row.row_data)
                db_resoponse.put(all_data)
            except:
                db_resoponse.put((None))
            s.close()
        elif ev[0] == 'delete':
            s = session()
            print(f"deleting {ev[1]}")
            try:
                r = s.query(Results).filter_by(date=ev[1]).delete()
                s.commit()
            except:
                print(f"Failed to delete {ev[1]}")
            s.close()
        else:
            print("Unknown command")
        ev = db_event.get()


def create_thread():
    global db_thread
    global db_event, db_resoponse
    if db_thread == None:
        print("creating thread")
        db_event = queue.Queue()
        db_resoponse = queue.Queue()
        db_thread = threading.Thread(target=db_thread_main)
        db_thread.start()


def store_results(answer_text, data, word_data):
    print("store data")
    global db_event
    create_thread()
    ev = ["store", json.dumps(answer_text), json.dumps(data), json.dumps(word_data)]
    db_event.put(ev)


def get_results(date=None):
    global db_event, db_resoponse
    create_thread()
    ev = ["get", date]
    db_event.put(ev)
    res_ev = db_resoponse.get()
    print(f"got result {res_ev}")
    return res_ev


def get_all():
    global db_event, db_resoponse
    create_thread()
    ev = ["get-all"]
    db_event.put(ev)
    res_ev = db_resoponse.get()
    print(f"got result {res_ev}")
    return res_ev


def delete_result(date):
    global db_event, db_resoponse
    create_thread()
    ev = ["delete", date]
    db_event.put(ev)


def db_quit():
    global db_thread
    if db_thread:
        ev = ["quit"]
        db_event.put(ev)
        db_thread.join()


def main():
    store_results("string", [("tears", ['absent', 'present', 'present', 'absent', 'absent']),
        ("panes", ['absent', 'correct', 'absent', 'correct', 'correct']),
        ("names", ['correct', 'correct', 'correct', 'correct', 'correct'])])
    rstr, rd = get_results(date.today().isoformat())
    for guess in rd:
        print(f"Word was {guess[0]}")
    db_quit()

if __name__ == "__main__":
    main()

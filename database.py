from email.contentmanager import raw_data_manager
import os
import sqlalchemy as db
from sqlalchemy import create_engine, select, Column, Integer, String, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from datetime import date
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'database.sqlite3')

Base = declarative_base()
class Results(Base):
    __tablename__ = "results_data"
    __table_args__ = (
        PrimaryKeyConstraint('date'),
    )
    date = Column(String, primary_key=True)
    result_string = Column(String)
    row_data = Column(String)
    
def store_results(answer_text, data):
    engine = create_engine(DATABASE_URI)
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)   
    s = session()
    r = s.query(Results).filter_by(date=date.today().isoformat()).first()
    if r:
        s.delete(r)
    r = Results(date=date.today().isoformat(), result_string=answer_text, row_data=json.dumps(data))
    s.add(r)
    s.commit()


def get_results(date=None):
    engine = create_engine(DATABASE_URI)
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    r = s.query(Results).filter_by(date=date).first()
    print(r.date)
    return r.result_string, json.loads(r.row_data)


def main():
    store_results("string", [("tears", ['absent', 'present', 'present', 'absent', 'absent']),
        ("panes", ['absent', 'correct', 'absent', 'correct', 'correct']),
        ("names", ['correct', 'correct', 'correct', 'correct', 'correct'])])
    rstr, rd = get_results(date.today().isoformat())
    for guess in rd:
        print(f"Word was {guess[0]}")

if __name__ == "__main__":
    main()

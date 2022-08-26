from flask import session
from . import app
from game import get_all_words, get_possible_words, pick_winning_word
import json

@app.route("/game/word_list")
def word_list():
    words = get_all_words()
    return {"res": "OK", "words": words}

@app.route("/game/start")
def start_word():
    word = pick_winning_word()
    session['winning_word'] = word
    print(session)
    return {"res": "OK", "word": word}

@app.route("/game/step/<word>")
def next_step(word):
    if 'winning_word' in session:
        print(f'Session winning word {session["winning_word"]}')
        return {"res": "OK", "result": ["absent", "absent", "absent", "absent", "absent"], "word_list": [], "actual_info": 3.5}
    else:
        return {"res": "No Session Data"}
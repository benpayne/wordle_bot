import random
import re
from word_work import get_all_words, get_possible_words 

yellow_box = u"\U0001f7e8"
green_box = u"\U0001f7e9"
grey_box = u"\u2b1c"

def pick_winning_word():
    words = get_possible_words()
    random.seed()
    i = random.randrange(len(words))
    return words[i]

def read_guess():
    valid = False
    print("Please guess a 5 letter word:")
    while not valid:
        word = input()
        if len(word) != 5:
            print("Word must be 5 letter long")
        elif word not in get_all_words():
            print("Not a valid word")
        else:
            valid = True
    return word

def print_result(word, states):
    string = ""
    for i, l in enumerate(word):
        if states[i] == 'correct':
            string += '\033[42m' + l + '\033[0m'
        elif states[i] == 'present':
            string += '\033[43m' + l + '\033[0m'
        else:
            string += l
    return string

def get_pattern(results):
    text = f"Wordle {len(results)}/6\n"
    for r in results:
        #print(f"row: {r}")
        for c in r[1]:
            if c == 'correct':
                text += green_box
            elif c == 'present':
                text += yellow_box
            else:
                text += grey_box
        text += '\n'
    return text


def compare_guess(winning_word, guess):
    results = ['absent'] * 5
    letters = []
    
    for i, c in enumerate(guess):
        if winning_word[i] == c:
            results[i] = 'correct'
        else:
            letters.append(winning_word[i])

    #print(f"remaining letters {letters}")
    for i, c in enumerate(guess):
        if results[i] == 'absent':
            if c in letters:
                results[i] = 'present'
                letters.remove(c)

    return results

def result_done(result):
    for r in result:
        if r != 'correct':
            return False
    return True

def main():
    winning_word = pick_winning_word()
    #print(f"Winning word is {winning_word}")

    won = False

    for i in range(6):
        guess = read_guess()
        result = compare_guess(winning_word, guess)
        print(print_result(guess, result))
        if result_done(result):
            won = True
            print("Congrats!!!!")
            break

    if not won:
        print(f"Failed, the word was {winning_word}")

if __name__ == "__main__":
    main()
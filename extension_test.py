
import wordle_fast
from word_work import get_all_words, letter_info

li = letter_info('h')
li.occurance = 1
li.locations.append(0)
res = wordle_fast.c_match(li, "hello")
print("result", res)

known_letters = {'h': li}
new_words = wordle_fast.c_filter(get_all_words(), known_letters)
print(new_words)

from hashlib import new
from operator import ge
import re
from game import pick_winning_word, compare_guess, result_done, print_result
from word_work import expected_information, build_work_freq_data, get_all_words, get_possible_words, letter_info, letter_state
from multiprocessing import Pool

class wordle_bot:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.known_letters = letter_state()
        self.word_list = get_all_words()

    def pick_best_word(self, word_list):
        return word_list[0]

    def generate_guess(self):
        if self.known_letters.empty():
            return "tears"
        else:
            self.word_list = self.known_letters.fliter_list(self.word_list)
            #for l, d in self.known_letters.known_letters.items():
            #    print(d)
            #print(self.word_list)
            if len(self.word_list) > 0:
                word = self.pick_best_word(self.word_list)
                if word not in self.word_list:
                    print(f"{word} not in list {self.word_list}")
                self.word_list.remove(word)
                return word
            else:
                print("Failed to find a valid word")
                return None

    def process_result(self, guess, result):
        self.known_letters.process_result(guess, result)

    #@profile
    def run(self, winning_word, print_res=False):
        for i in range(6):
            guess = self.generate_guess()
            result = compare_guess(winning_word, guess)
            self.process_result(guess, result)
            if print_res:
                print_result(guess, result)
            if result_done(result):
                return i + 1
        # failed
        return -1

def test():
    li = letter_info('s')
    li.occurance = 1
    li.locations.add(0)

    sim = wordle_bot()

    assert li.match("sleep") == True
    li.letter = 'e'
    assert li.match("sleep") == False
    li.occurance = 2
    li.locations = set()
    li.locations.add(2)
    assert li.match("sleep") == True
    li.letter = 's'
    assert li.match("sleep") == False

    li.occurance = 1
    li.or_more = False
    assert li.match("sleep") == False

    li.occurance = 1
    li.or_more = False
    li.locations = set()
    li.letter = 'e'
    assert li.match("sleep") == False

    res = ['correct', 'absent', 'present', 'absent', 'present']
    sim.process_result("sleep", res)
    print(f"e: {sim.known_letters['e']}")
    print(f"s: {sim.known_letters['s']}")
    print(f"l: {sim.known_letters['l']}")
    print(f"p: {sim.known_letters['p']}")

    assert len(sim.known_letters) == 4
    assert 's' in sim.known_letters.keys()
    assert 'l' in sim.known_letters.keys()
    assert 'e' in sim.known_letters.keys()
    assert 'p' in sim.known_letters.keys()
    assert sim.known_letters['e'].or_more == False
    assert sim.known_letters['e'].occurance == 1
    assert sim.known_letters['s'].occurance == 1
    assert sim.known_letters['s'].or_more == True
    assert len(sim.known_letters['s'].locations) == 1
    assert sim.known_letters['l'].or_more == False
    assert sim.known_letters['l'].occurance == 0
    assert sim.known_letters['p'].or_more == True
    assert sim.known_letters['p'].occurance == 1
 
    guess = sim.generate_guess()
    print(f"guess: {guess}")
    assert guess == 'scape'


import json

class weighted_words(wordle_bot):
    def __init__(self) -> None:
        super().__init__()
        fp = open("data/freq_map.txt", "r")
        self.word_data = json.load(fp)

    def pick_best_word(self, word_list):
        words = {}
        highest = 0
        highest_word = None
        for w in word_list:
            if w in self.word_data:
                words[w] = self.word_data[w]
            else:
                words[w] = 0
            if words[w] > highest:
                highest = words[w]
                highest_word = w
            elif highest_word == None:
                highest_word = w

        return highest_word

class expected_info(wordle_bot):
    def __init__(self) -> None:
        super().__init__()
        self.word_freq = build_work_freq_data()

    def pick_best_word(self, word_list):
        words = {}
        highest = 0
        highest_word = None
        for w in word_list:
            info = expected_information(word_list, w) * self.word_freq.loc[w]['weights']
            if info > highest:
                highest = info
                highest_word = w
            elif highest_word == None:
                highest_word = w

        return highest_word


def main():
    all_words = get_possible_words()

    with Pool(8) as executor:
        results = executor.map(run_once, all_words)

    buckets = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, -1: 0}
    for r in results:
        buckets[r] += 1

    #print("\033[H\033[J", end="")
    #print(f"{i}/{len(all_words)} {buckets} - {word}")
    print(buckets)
    print(f"Failed {buckets[-1]/len(all_words)*100:0.2f}%")
    score = (buckets[1] + (2 * buckets[2]) + (3 * buckets[3]) + (4 * buckets[4]) + (5 * buckets[5]) + (6 * buckets[6])) / (len(all_words) - buckets[-1])
    print(f"Average Rating {score:0.2f}")


#@profile
def run_once(winning_word, print_res=False):
    if print_res: 
        print(f"Winning word is {winning_word}")

    #sim = weighted_words()
    sim = expected_info()
    res = sim.run(winning_word, print_res=print_res)
    print("\033[H\033[J", end="")
    print(f"{winning_word} - {res}")
    if res > 0:
        if print_res: 
            print(f"Congrats won in {res} rounds!!!!")
        return res
    else:
        if print_res:
            print(f"Failed, the word was {winning_word}") 
        return -1



if __name__ == "__main__":
    main()
    #run_once(pick_winning_word(), True)
    #test()


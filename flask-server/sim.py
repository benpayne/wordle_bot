import argparse
from copyreg import pickle
import re
from game import compare_guess, result_done, print_result, pick_winning_word
from word_work import expected_information, build_work_freq_data, get_all_words, get_possible_words, letter_info, letter_state, probability_to_entrope, get_word_weight
from multiprocessing import Pool
import os

class wordle_bot:
    start_word = os.getenv("WOBOT_START_WORD")
    
    def __init__(self, print_res = False) -> None:
        self.reset()
        self.print_res = print_res

    def reset(self):
        self.known_letters = letter_state()
        self.word_list = get_all_words()
        self.actual_info = 0.0
        self.total_info = 0.0

    def pick_best_word(self, word_list, round):
        return word_list[0]

    def generate_guess(self, round):
        if self.known_letters.empty():
            #print(f"start word is {self.start_word}")
            if self.start_word is None:
                return 'tears'
            else:
                return self.start_word
        else:
            word_list_orig = len(self.word_list)
            self.word_list = self.known_letters.fliter_list(self.word_list)
            self.actual_info = probability_to_entrope(len(self.word_list)/word_list_orig)
            self.total_info += self.actual_info
            if self.print_res:
                print(f"actual information: {self.actual_info:0.2f}, total information: {self.total_info:0.2f}")
            #for l, d in self.known_letters.known_letters.items():
            #    print(d)
            #print(self.word_list)
            if len(self.word_list) > 0:
                word = self.pick_best_word(self.word_list, round)
                if word in self.word_list:
                   self.word_list.remove(word)
                return word
            else:
                print("Failed to find a valid word")
                return None

    def process_result(self, guess, result):
        self.known_letters.process_result(guess, result)

    #@profile
    def run(self, winning_word):
        for i in range(6):
            guess = self.generate_guess(i)
            result = compare_guess(winning_word, guess)
            self.process_result(guess, result)
            if self.print_res:
                print(print_result(guess, result))
            if result_done(result):
                return i + 1
        # failed
        return -1




import json

class weighted_words(wordle_bot):
    def __init__(self) -> None:
        super().__init__()
        fp = open("data/freq_map.txt", "r")
        self.word_data = json.load(fp)

    def pick_best_word(self, word_list, round):
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
    def __init__(self, print_list=False, threshold_one=7, threshold_two=10) -> None:
        super().__init__(print_list)
        self.word_freq = build_work_freq_data()
        self.print_list = print_list
        self.word_list_data = {}
        self.threshold_one = threshold_one
        self.threshold_two = threshold_two
        words = get_first_words("all")
        for key, data in words.items():
            self.word_list_data[key] = {'exp_info': data['exp_info'], 'word_freq': data['word_weight'], 'rank': data['exp_info']}

    def pick_best_word(self, word_list, round):
        def map_fn(word):
            d = self.word_freq.loc[word]
            return expected_information(word_list, word), d['weights'], d['rank']

        #all_words = get_all_words()
        all_words = word_list
        weights = map(map_fn, all_words)
        highest = 0
        highest_word = None
        highest_data = None
        word_data = {}
        #print(f"total_info {self.total_info}")
        for i, w in enumerate(weights):
            if self.total_info < self.threshold_two:
                p = w[0]
            elif self.total_info < self.threshold_one:
                p = w[0] * w[1]
            else:
                p = w[2]
            word_data[all_words[i]] = [w[0], w[1], p]
            if p > highest or highest_word == None:
                highest = p
                highest_word = all_words[i]
                highest_data = w
        if self.print_list:
            self.word_list_data = {}
            for word_key, data in sorted(word_data.items(), key = lambda x: x[1][2], reverse=True):
                print(f"{word_key} -> ({data[0]:0.2f}, {data[1]:0.2f}) = {data[2]:0.2f}, ", end='')
                self.word_list_data[word_key] = {'exp_info': data[0], 'word_freq': data[1], 'rank': data[2]}
            print("")
            print(f"highest word is {highest_word}, expected info: {highest_data[0]:0.2f}, word freq {highest_data[1]:0.4f}") 
        return highest_word


def run_all_words():
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
    sim = expected_info(print_list=print_res)
    res = sim.run(winning_word)
    if not print_res:
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


def map_fn_exp_info_all(word):
    res = expected_information(get_all_words(), word)
    print("\033[H\033[J", end="")
    print(f"{word} -> {res}")
    return res

def map_fn_exp_info_answers(word):
    res = expected_information(get_possible_words(), word)
    print("\033[H\033[J", end="")
    print(f"{word} -> {res}")
    return res


def run_first_word():
    word_list = get_all_words()

    word_freq = build_work_freq_data()
    with Pool(8) as executor:
        results = executor.map(map_fn_exp_info_all, word_list)

    res_dict = {}
    for i, res in enumerate(results):
        word = word_list[i]
        #print(f"index {i}, word {word}, res {res}")
        res_dict[word] = {'exp_info': res, 'word_weight': word_freq.loc[word]['weights']}

    first_word_data_file = open("first_word_data_all.json", "w")
    json.dump(res_dict, first_word_data_file)

    with Pool(8) as executor:
        results = executor.map(map_fn_exp_info_answers, word_list)

    res_dict = {}
    for i, res in enumerate(results):
        word = word_list[i]
        #print(f"index {i}, word {word}, res {res}")
        res_dict[word] = {'exp_info': res, 'word_weight': word_freq.loc[word]['weights']}

    first_word_data_file = open("first_word_data_answers.json", "w")
    json.dump(res_dict, first_word_data_file)


def get_first_words(list_name, count=-1, sort='exp_info'):
    try: 
        first_word_data_file = open(f"first_word_data_{list_name}.json", "r")
        res_dict = json.load(first_word_data_file)
    except Exception as e:
        print(e)

    if count < 0:
        sorted_res = dict(sorted(res_dict.items(), key=lambda item: item[1][sort], reverse=True))
    else:
        sorted_res = dict(sorted(res_dict.items(), key=lambda item: item[1][sort], reverse=True)[:count])

    return sorted_res


def get_first_word_stats(list_name, word):
    try: 
        first_word_data_file = open(f"first_word_data_{list_name}.json", "r")
        res_dict = json.load(first_word_data_file)
    except Exception as e:
        print(e)
    
    sorted_res = sorted(res_dict.items(), key=lambda item: item[1]['exp_info'], reverse=True)
    for i, row in enumerate(sorted_res):
        if row[0] == word:
            return i, row[1]
    
    return -1, None


def dump_first_words(list, count):
    sorted_res = get_first_words(list, count)
    for k, data in sorted_res.items():
        print(f"{k} -> {data['exp_info']:0.2f} : {data['word_weight']:0.2f}")


def check_first_word(list, word):
    i, word_data = get_first_word_stats(list, word)
    print(f"{word}({i}) -> {word_data['exp_info']:0.2f}, weight {word_data['word_weight']:0.2f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--once', action='store_true', help='run the simulaton on one random word')
    parser.add_argument('-f', '--first', action='store_true', help='generate first word data')
    parser.add_argument('-l', '--list', choices=('all', 'answers'), help='list of first words, all or answers')
    parser.add_argument('-c', '--count', type=int, help='count of words to dump')
    parser.add_argument('-w', '--word', help='run the simulaton on the specified word')
    parser.add_argument('-s', '--start_word', help='run the simulaton on the specified start word')
    args = parser.parse_args()

    print(args)

    word_list = 'all'
    if args.list:
        word_list = args.list

    if args.start_word:
        print(f"setting start work to {args.start_word}")
        os.environ["WOBOT_START_WORD"] = args.start_word
    
    if args.once:
        if args.word:
            run_once(args.word, True)
        else:
            run_once(pick_winning_word(), True)
    elif args.first:
        if args.word:
            check_first_word(word_list, args.word)
        elif args.count:
            dump_first_words(word_list, args.count)
        else:
            run_first_word()
    else:
        run_all_words()

if __name__ == "__main__":
    main()


import argparse
from game import compare_guess, result_done, print_result, pick_winning_word
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
        def map_fn(word):
            return expected_information(word_list, word), self.word_freq.loc[word]['weights']

        weights = map(map_fn, word_list)
        highest = 0
        highest_word = None
        for i, w in enumerate(weights):
            p = w[0] * w[1]
            print(f"{word_list[i]} -> ({w[0]:0.2f}, {w[1]:0.2f}) = {p:0.2f}, ", end='')
            if p > highest or highest_word == None:
                highest = p
                highest_word = word_list[i]
        print(f" highest word is {highest_word}")
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
    sim = expected_info()
    res = sim.run(winning_word, print_res=print_res)
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--once', action='store_true', help='run the simulaton on one random word')
    parser.add_argument('-w', '--word', help='run the simulaton on the specified word')
    args = parser.parse_args()

    print(args)

    if args.word:
        run_once(args.word, True)
    elif args.once:
        run_once(pick_winning_word(), True)
    else:
        run_all_words()


if __name__ == "__main__":
    main()


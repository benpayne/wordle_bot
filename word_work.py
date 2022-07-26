import json
from math import log
import re
from unittest import result

#from game import result_done

def get_words():
    with open('data/sgb-words.txt','r') as f:
        words = f.read().splitlines()

    return words

def get_all_words():
    with open('data/allowed_words.txt','r') as f:
        words = f.read().splitlines()

    return words

def get_possible_words():
    with open('data/possible_words.txt','r') as f:
        words = f.read().splitlines()

    return words


word_freq = None
def get_word_weight(word):
    global word_freq
    if word_freq == None:
        fp = open("data/freq_map.txt", "r")
        word_freq = json.load(fp)
    if word in word_freq:
        return word_freq[word]
    else:
        return 0


# known_letters is a dict of letters as keys with letter_info as data:
#  occurance - 1, 2, 3
#  or_more - if we know exactly the number or it's x or more, set when we see an absent on a doulble, tripple letter guess
#  locations - array of known locations, max known_occurance in size.
class letter_info:
    def __init__(self, letter) -> None:
        self.occurance = 0
        self.or_more = True
        self.locations = set()
        self.letter = letter

    def set_location(self, i):
        if i not in self.locations:
            self.locations.add(i)
        assert len(self.locations) <= self.occurance

    def match(self, word):
        count = 0
        locations = set()
        for i, l in enumerate(word):
            if l == self.letter:
                locations.add(i)
                count += 1
        if self.or_more and count < self.occurance:
            return False
        if not self.or_more and count != self.occurance:
            return False
        for i in self.locations:
            if word[i] != self.letter:
                return False
        return True

    def __str__(self):
        return f"occurance: {self.occurance}, or_more: {self.or_more}, locations: {self.locations}"


class letter_state:
    def __init__(self) -> None:
        self.known_letters = {}

    def empty(self):
        return len(self.known_letters) == 0

    def process_result(self, guess, result):
        new_state = {}
        for i, state in enumerate(result):
            li = None
            if guess[i] not in new_state:
                li = letter_info(guess[i])
                new_state[guess[i]] = li
            else:
                li = new_state[guess[i]]

            if state == 'correct':
                li.occurance += 1
                li.locations.add(i)
            elif state == 'present':
                li.occurance += 1
            elif state == 'absent':
                li.or_more = False

        # merge current state with global state
        for letter, li in new_state.items():
            if letter in self.known_letters:
                old_li = self.known_letters[letter]
                if old_li.or_more == True and li.or_more == False:
                    old_li.or_more = False
                if old_li.occurance < li.occurance:
                    old_li.occurance = li.occurance
                for i in li.locations:
                    old_li.set_location(i)
            else:
                self.known_letters[letter] = li

    def fliter_list(self, word_list):
        new_words = []
        for word in word_list:
            add_word = True
            for l, li in self.known_letters.items():
                if not li.match(word):
                    add_word = False
            if add_word:
                new_words.append(word)
        return new_words


def words_with_letter( list, letter, pos=-1 ):
    remaining = []
    for word in list:
        if pos >= 0:
            if word[pos] == letter:
                remaining.append(word)
        else:
            if letter in word:
                remaining.append(word)
    return remaining

def words_without_letter( list, letter ):
    remaining = []
    for word in list:
        if letter not in word:
            remaining.append(word)
    return remaining

def words_with_letters(word_list, letters, mask):
    remaining = []
    unused = letters.copy()
    for word in word_list:
        #print(f"word {word}, {list(word)}")
        for i, l in enumerate(list(word)):
            #print(f"Word: {word}, i {i}, l {l}")
            if mask[i] == '_':
                if l in unused:
                    unused.remove(l)
        #print(f"Done: {letters}")
        if len(unused) == 0:
            remaining.append(word)
    return remaining


def result_to_number(result):
    # 3 state, 5 bit number
    # first result is lowest bit
    total = 0
    for i, v in enumerate(result):
        value = 0
        if v == 'correct':
            value = 2
        elif v == 'present':
            value = 1
        total += value * (3**(i))
        #print(value, total, (3**(i)))
    return total

def number_to_result(num):
    result = []
    for i in range(5):
        if num % 3 == 2:
            result.append('correct')
        elif num % 3 == 1:
            result.append('present')
        else:
            result.append('absent')
        num //= 3
    return result

def result_done(result):
    for r in result:
        if r != 'correct':
            return False
    return True


def expected_information(word_list, word):
    # generate derived word list for all 243 permutations of the result, 
    # track the number of words in each list
    # probability of finding the word is bucket list size / total list size
    # Entropy of that is log2(1/p) assgin that to the bucket 
    # take a weight average of each bucket wieghted by probability of that being the answer

    result = ['absent'] * 5
    buckets = []
    while not result_done(result):
        ls = letter_state()
        ls.process_result(word, result)
        buckets.append(len(ls.fliter_list(word_list)))
        #print(result)
        for i in range(5):
            if result[i] == 'correct':
                result[i] = 'absent'
                # carry to next bit
            elif result[i] == 'absent':
                result[i] = 'present'
                break
            elif result[i] == 'present':
                result[i] = 'correct'
                break
    # append one for winning word
    buckets.append(1)

    total = 0
    sum = 0
    for b in buckets:
        p = b / len(word_list)
        if p > 0:
            i = log(1/p, 2)
            total += p*i
            sum += p

    #print(f"{total/sum}")
    #print(buckets)
    return total/sum

def letter_frequency():

    with open('data/allowed_words.txt','r') as f:
        words = f.read().splitlines()

    first = {}
    second = {}
    third = {}
    fourth = {}
    fifth = {}
    for w in words:
        if w[0] in first:
            first[w[0]] += 1
        else:
            first[w[0]] = 1
        
        if w[1] in second:
            second[w[1]] += 1
        else:
            second[w[1]] = 1

        if w[2] in third:
            third[w[2]] += 1
        else:
            third[w[2]] = 1

        if w[3] in fourth:
            fourth[w[3]] += 1
        else:
            fourth[w[3]] = 1

        if w[4] in fifth:
            fifth[w[4]] += 1
        else:
            fifth[w[4]] = 1


    print(f"First: {sorted(first.items(), key=lambda item: item[1], reverse=True)[0:3]}")
    print(f"second: {sorted(second.items(), key=lambda item: item[1], reverse=True)[0:3]}")
    print(f"third: {sorted(third.items(), key=lambda item: item[1], reverse=True)[0:3]}")
    print(f"fourth: {sorted(fourth.items(), key=lambda item: item[1], reverse=True)[0:3]}")
    print(f"fifth: {sorted(fifth.items(), key=lambda item: item[1], reverse=True)[0:3]}")

def word_freq_test():
    words = get_all_words()
    weights = {}
    for w in words:
        weights[w] = get_word_weight(w)
    weight_sorted = sorted(weights.items(), key=lambda item: item[1], reverse=True)
    print(f"Total word count {len(weight_sorted)}")
    print(f"Top words {weight_sorted[:10]}")
    print(f"2k words {weight_sorted[2000:2010]}")
    print(f"3k words {weight_sorted[3000:3010]}")
    print(f"4k words {weight_sorted[4000:4010]}")
    print(f"5k words {weight_sorted[5000:5010]}")
    print(f"6k words {weight_sorted[6000:6010]}")


def exp_info_test():
    word = "crane"
    value = expected_information(get_all_words(), word)
    print(f"Expected Information from \"{word}\" is {value:0.2f}")

def result_test():
    res = number_to_result(4)
    print(res)
    num = result_to_number(res)
    print(num)
    for i in range(3**5):
        assert result_to_number(number_to_result(i)) == i

if __name__ == "__main__":
    #word_freq_test()
    #exp_info_test()
    result_test()

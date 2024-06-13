import random
import pandas as pd
import string

debug = False

class wordle:
    def __init__(self, wordlist_txt_file, method, trials=2):
        self.wl = wordlist_txt_file
        self.trials = trials
        self.word_list = None
        self.available_positions = []
        self.guessed_word_dict = dict()
        self.char_failed_position = dict()
        self.filtered_word_list = []
        self.temp_filtered_word_list = []
        self.attempt_num_in_current_trial = -1
        self.successCount = {
            "successes": 0,
            "failures": 0,
            "guesses": 0
        }
        self.attemptCount = {
            "tries1": 0,
            "tries2": 0,
            "tries3": 0,
            "tries4": 0,
            "tries5": 0,
            "tries6": 0
        }
        self.method = method

    def get_wl(self):
        word_list = []
        with open(self.wl, 'r') as file:
            for line in file:
                word_list.append(line.strip().lower())
        self.word_list = word_list

    def pick_random_target_word(self):
        if self.word_list == None:
            self.get_wl()
        #word_list = self.df_wl
        return random.choice(self.word_list)

    def update_char_failed_position(self, char, position):
        print(f'char={char} position={position}')
        if char not in self.char_failed_position.keys():
        #    self.char_failed_position[char].append(position)
        #else:
            self.char_failed_position[char] = []
        self.char_failed_position[char].append(position)
        self.char_failed_position[char] = [*{s for s in self.char_failed_position[char]},]
        #filter the filtered_word_list further excluding the character at a failed position
        print(f'self.char_failed_position={self.char_failed_position}')
        #print(f'self.filtered_word_list before = {self.filtered_word_list}')
        if not isinstance(self.filtered_word_list, type(None)):
            self.filtered_word_list = [ele for ele in self.filtered_word_list if ele[position] != char]
            self.temp_filtered_word_list = self.filtered_word_list
        #print(f'self.filtered_word_list after = {self.filtered_word_list}')

    def get_user_guess(self):
        while True:
            guess = input("Enter your 5-letter word guess: ").strip().lower()
            if len(guess) != 5 or not guess.isalpha():
                print("Please enter a valid 5-letter word.")
            else:
                return guess

    def calculate_feedback(self, guess, target):
        '''feedback = ""
        for i in range(len(guess)):
            if guess[i] == target[i]:
                feedback += guess[i].upper()
            elif guess[i] in target:
                feedback += guess[i].lower()
            else:
                feedback += "*"
        return feedback'''
        feedback = ["*"] * len(target)
        used_indices = set()

        for i in range(len(guess)):
            if guess[i] == target[i]:
                feedback[i] = guess[i].upper()
                used_indices.add(i)

        for i in range(len(guess)):
            if guess[i] != target[i] and guess[i] in target:
                for j in range(len(target)):
                    if target[j] == guess[i] and j not in used_indices and guess[j] != target[j]:
                        feedback[i] = guess[i].lower()
                        used_indices.add(j)
                        break

        return ''.join(feedback)

    def print_missing_chars(self, missing_chars):
        if missing_chars:
            print("Missing characters:")
            sorted_missing_chars = sorted(set(missing_chars))
            print(" ".join(sorted_missing_chars))
        else:
            print("All guessed characters are in the Wordle word!")

    def get_available_positions(self, uchar_dict):
        available_positions = [0, 1, 2, 3, 4]
        if len(uchar_dict) > 0:
            positions_occupied = []
            for k in uchar_dict.keys():
                for val in uchar_dict[k]:
                    positions_occupied.append(val)
            #positions_occupied = list(uchar_dict.values())
            available_positions = [x for x in available_positions if x not in positions_occupied]
            if debug:
                print(f'positions_occupied={positions_occupied}')
                print(f'available_positions={available_positions}')
        else:
            print(f'empty uchar_dict')
            print(f'available_positions={available_positions}')
        self.available_positions = available_positions

    def get_char_positional_prob_dict(self, lchar_dict, other_possible_char_list, uchar_dict):
        lchar_positional_prob_dict = dict()
        ochar_positional_prob_dict = dict()
        #print(f'lchar={lchar}')
        if debug:
            print(f'uchar_dict={uchar_dict}')
            print(f'len(filtered_word_list)={len(self.filtered_word_list)}')
            print(f'len(uchar_dict)={len(uchar_dict)}')
        if len(self.available_positions) == 0:
            self.get_available_positions(uchar_dict)
        for key in lchar_dict:
            positional_prob_dict = dict()
            for available_position in self.available_positions:
                temp_filtered_list = [ele for ele in self.temp_filtered_word_list if ele[available_position] == key]
                if len(self.temp_filtered_word_list) == 0:
                    self.temp_filtered_word_list = self.filtered_word_list
                    temp_filtered_list = [ele for ele in self.temp_filtered_word_list if ele[available_position] == key]
                if len(self.temp_filtered_word_list) == 0:
                    print(f'key={key} available_position={available_position}')
                    print(f'temp_filtered_list={temp_filtered_list} self.temp_filtered_word_list={self.temp_filtered_word_list}')
                    #exit(0)
                    #debug = True
                if debug:
                    print(f'available_position={available_position}')
                    print(f'len(temp_filtered_list)={len(temp_filtered_list)}')

                #if len(temp_filtered_list) == 0:
                #    positional_prob_dict[available_position] = 0
                #else:
                if len(self.temp_filtered_word_list) > 0:
                    positional_prob_dict[available_position] = len(temp_filtered_list)/len(self.temp_filtered_word_list)
                else:
                    positional_prob_dict[available_position] = 0.0
            lchar_positional_prob_dict[key] = positional_prob_dict
        if debug:
            print(f'lchar_positional_prob_dict={lchar_positional_prob_dict}')

        for char in other_possible_char_list:
            positional_prob_dict = dict()
            for available_position in self.available_positions:
                #print(f'available_position={available_position}')
                temp_filtered_list = [ele for ele in self.temp_filtered_word_list if ele[available_position] == char]
                if len(self.temp_filtered_word_list) == 0:
                    self.temp_filtered_word_list = self.filtered_word_list
                    temp_filtered_list = [ele for ele in self.temp_filtered_word_list if ele[available_position] == char]
                #print(f'len(temp_filtered_list)={len(temp_filtered_list)}')
                #if len(temp_filtered_list) == 0:
                #    positional_prob_dict[available_position] = 0
                #else:
                if len(self.temp_filtered_word_list) > 0:
                    positional_prob_dict[available_position] = len(temp_filtered_list)/len(self.temp_filtered_word_list)
                else:
                    positional_prob_dict[available_position] = 0.0
            ochar_positional_prob_dict[char] = positional_prob_dict
        #print(f'ochar_positional_prob_dict={ochar_positional_prob_dict}')
        return lchar_positional_prob_dict, ochar_positional_prob_dict

    def get_word_from_guessed_dict(self):
        guessed_word = ''
        sorted_dict = dict(sorted(self.guessed_word_dict.items()))
        #print(f'sorted_dict={sorted_dict}')

        for i in sorted_dict:
            #print('here2')
            #print(i, self.guessed_word_dict[i])
            guessed_word += self.guessed_word_dict[i]
        return guessed_word

    def get_most_probable_char(self, prob_dict, position):
        char = ''
        prob = 0.0
        #print(f'prob_dict={prob_dict}')
        for key in prob_dict:
            #print(f'key={key}')
            for k in prob_dict[key]:
                #print(f'k={k}')
                if k==position and prob_dict[key][k] > prob:
                    prob = prob_dict[key][k]
                    char = key
            #print(f'char={char} prob={prob}')
            #exit(0)

        return char, prob

    def get_positional_prob_dict_excluding_failed_positions(self, prob_dict, char):
        return_dict = dict()
        if debug:
            print(prob_dict, char)
        return_dict = prob_dict
        for key, val_list in self.char_failed_position.items():
            for val in val_list:
                if debug:
                    print(f'key={key}, val={val} char={char} self.char_failed_position={self.char_failed_position}')
                if key == char:
                    #return_dict = prob_dict.pop(self.char_failed_position[key])
                    #for k, v in self.char_failed_position:
                    #print(f'k={k} v={v}')
                    #print(f'self.char_failed_position[key]={self.char_failed_position[key]}')
                    if debug:
                        print(f'return_dict={return_dict}')
                    if val in return_dict:
                        del return_dict[val]#self.char_failed_position[val]] #self.char_failed_position[key]
                    #return_dict = prob_dict
        if debug:
            print(f'return_dict={return_dict}')
        #exit(0)
        return return_dict

    def heuristic_random(self, lchar_positional_prob_dict, ochar_positional_prob_dict):
        if len(self.filtered_word_list) == 0:
            return self.get_word_from_guessed_dict()

        return random.choice(self.filtered_word_list)

    def heuristic_probabilistic(self, lchar_positional_prob_dict, ochar_positional_prob_dict, uchar_dict, lchar_dict, other_possible_char_list):
        word_score_dict = dict()
        prob_score = 1.0
        if debug:
            print(f'self.guessed_word_dict={self.guessed_word_dict}')
        self.temp_filtered_word_list = self.filtered_word_list
        for key in lchar_positional_prob_dict:
            if len(self.get_word_from_guessed_dict()) == 5: #len(self.guessed_word_dict) == 5:
                guessed_word = self.get_word_from_guessed_dict()
                return guessed_word
            #if len(self.guessed_word_dict) == 5:
            #    return self.get_word_from_guessed_dict()
            if debug:
                print(key)

            positional_prob_dict = lchar_positional_prob_dict[key]
            if debug:
                print(f'positional_prob_dict={positional_prob_dict}')
            positional_prob_dict_excluding_failed_positions = self.get_positional_prob_dict_excluding_failed_positions(positional_prob_dict, key)
            try:
                if len(positional_prob_dict_excluding_failed_positions) > 0:
                    k, v = max(positional_prob_dict_excluding_failed_positions.items(), key=lambda k: k[1])
                    if len(self.available_positions) == 0:
                        self.get_available_positions(uchar_dict)
                    if debug:
                        print(f'available_positions={self.available_positions}')
                        print(f'k={k} v={v}')
                    prob_score *= v
                    #exit(0)
                    self.temp_filtered_word_list = [ele for ele in self.temp_filtered_word_list if ele[k] == key]
                    if len(self.temp_filtered_word_list) == 0:
                        self.temp_filtered_word_list = [ele for ele in self.filtered_word_list if ele[k] == key]
                    if len(self.temp_filtered_word_list) == 1:
                        return self.temp_filtered_word_list[0]
                    if debug:
                        print(f'len(filtered_word_list)={len(self.filtered_word_list)}')
                        print(f'prob_score={prob_score}')
                    if len(key) == 0:
                        print(f'key is blank.')
                        exit(0)
                    else:
                        self.guessed_word_dict[k] = key
                    if debug:
                        print(f'self.guessed_word_dict={self.guessed_word_dict}')
                    self.available_positions.remove(k)
                    if debug:
                        print(f'available_positions={self.available_positions}')
                    lchar_positional_prob_dict, ochar_positional_prob_dict = self.get_char_positional_prob_dict(lchar_dict, other_possible_char_list, uchar_dict)

            except Exception as error:
                print("An exception occurred:", error)

        #if len(self.guessed_word_dict) == 5:
        #    return self.get_word_from_guessed_dict()

        '''if len(self.get_word_from_guessed_dict()) == 5: #len(self.guessed_word_dict) == 5:
            guessed_word = self.get_word_from_guessed_dict()
            return guessed_word'''

        if len(ochar_positional_prob_dict) > 0:
            for key in ochar_positional_prob_dict:
                for position in self.available_positions:
                    if debug:
                        print(key)
                    most_probable_char, char_prob = self.get_most_probable_char(ochar_positional_prob_dict, position)
                    #positional_prob_dict = ochar_positional_prob_dict[key]
                    #print(f'positional_prob_dict={positional_prob_dict}')
                    #k, v = max(positional_prob_dict.items(), key=lambda k: k[1])
                    if len(self.available_positions) == 0:
                        self.get_available_positions(uchar_dict)
                    if debug:
                        print(f'available_positions={self.available_positions}')
                    #print(f'k={k} v={v}')
                    prob_score *= char_prob #v
                    self.temp_filtered_word_list = [ele for ele in self.temp_filtered_word_list if ele[position] == most_probable_char]
                    if len(self.temp_filtered_word_list) == 0:
                        self.temp_filtered_word_list = [ele for ele in self.filtered_word_list if ele[position] == most_probable_char]
                    if len(self.temp_filtered_word_list) == 1:
                        return self.temp_filtered_word_list[0]
                    if debug:
                        print(f'len(filtered_word_list)={len(self.filtered_word_list)}')
                        print(f'prob_score={prob_score}')
                    if most_probable_char == '':
                        print(f'most_probable_char is blank.')
                        #exit(0)
                    else:
                        self.guessed_word_dict[position] = most_probable_char
                    if debug:
                        print(f'self.guessed_word_dict={self.guessed_word_dict}')
                    self.available_positions.remove(position)
                    if debug:
                        print(f'available_positions={self.available_positions}')
                    if len(self.get_word_from_guessed_dict()) == 5: #len(self.guessed_word_dict) == 5:
                        guessed_word = self.get_word_from_guessed_dict()
                        return guessed_word

    def next_guess(self, feedback, missing_chars):
        if debug:
            print(feedback)
            print(missing_chars)
        uchar_dict = dict()
        uchar_index = 0
        if isinstance(self.filtered_word_list, type(None)):
            self.filtered_word_list = self.word_list
        for ele in feedback:
            if ele.isupper():
                if ele not in uchar_dict:
                    uchar_dict[ele] = []
                uchar_dict[ele].append(uchar_index)
                #uchar_dict.update({ele: uchar_index})
                self.guessed_word_dict[uchar_index] = ele.lower()
            uchar_index += 1
        #if debug:
        print(f'uchar_dict={uchar_dict} self.guessed_word_dict={self.guessed_word_dict}')
        lchar_dict = dict()
        lchar_index = 0
        for ele in feedback:
            if ele.islower():
                lchar_dict.update({ele: lchar_index})
                self.update_char_failed_position(ele, lchar_index)
                print(f'lchar_index={lchar_index}')
            lchar_index += 1
        if debug:
            print(f'lchar_dict={lchar_dict}')
        char_dict_list = [dict() for x in range(5)]
        char_dict_prob_list = [dict() for x in range(5)]
        #print(f'char_dict_list={char_dict_list}')
        #if self.attempt_num_in_current_trial == 1:
        #    self.filtered_word_list = self.word_list
        if debug:
            print(f'Before filtering len(filtered_word_list)={len(self.filtered_word_list)}')
        for key in uchar_dict.keys():
            print(f'key={key} uchar_dict[key]={uchar_dict[key]}')
            for val in uchar_dict[key]:
                self.filtered_word_list = [ele for ele in self.filtered_word_list if ele[val] == key.lower()]
                self.guessed_word_dict[val] = key.lower()
            #exit(0)
            #self.filtered_word_list = [ele for ele in self.filtered_word_list if ele[uchar_dict[key]] == key.lower()]

        if debug:
            print(f'len(filtered_word_list)={len(self.filtered_word_list)}')
        '''for key in lchar_dict.keys():
            # print(f'key={key} uchar_dict[key]={uchar_dict[key]}')
            filtered_word_list = [ele for ele in filtered_word_list if key in ele] #filter(lambda k: k in filtered_word_list and k[uchar_dict[key]:uchar_dict[key]] == key)
            # for el in filtered_word_list:
            #    print(el[uchar_dict[key]])'''
        #print(f'filtered_word_list before missing chars = {self.filtered_word_list}')
        for k in range(5):
            self.filtered_word_list = [ele for ele in self.filtered_word_list if ele[k] not in missing_chars]
        #print(f'filtered_word_list after removing missing chars = {self.filtered_word_list}')
        if debug:
            print(f'filtered_word_list={self.filtered_word_list}')
            print(f'len(filtered_word_list)={len(self.filtered_word_list)}')
        for i in range(len(self.filtered_word_list)):
            word = self.filtered_word_list[i]
            #print(word)
            for j in range(5):
                #print(word, word[j])
                if word[j] not in char_dict_list[j].keys():
                    char_dict_list[j].update({word[j]:1})
                else:
                    char_dict_list[j][word[j]] += 1
        #print(char_dict_list)
        for k in range(5):
            sum_val = sum(char_dict_list[k].values())
            for key in char_dict_list[k].keys():
                prob = char_dict_list[k][key]/sum_val
                char_dict_prob_list[k].update({key:prob})
        if debug:
            print(char_dict_prob_list)

        #for key in lchar_dict:
        #    print(f'key={key}')
        #lchar_positional_prob_dict = self.get_char_positional_prob_dict(filtered_word_list, lchar_dict, uchar_dict)

        #other_possible_char_list = []
        alphabets = list(string.ascii_lowercase)  #UnicodeSet('[a-z]')
        #print(alphabets)
        other_possible_char_list = [char for char in alphabets if char not in missing_chars and char not in list(uchar_dict.keys()) and char not in list(lchar_dict.keys())]
        self.temp_filtered_word_list = self.filtered_word_list
        if debug:
            print(f'other_possible_char_list={other_possible_char_list}')
        lchar_positional_prob_dict, ochar_positional_prob_dict = self.get_char_positional_prob_dict(lchar_dict, other_possible_char_list, uchar_dict)
        if debug:
            print(f'lchar_positional_prob_dict={lchar_positional_prob_dict}')
            print(f'ochar_positional_prob_dict={ochar_positional_prob_dict}')

        if self.method == 'random':
            guessed_word = self.heuristic_random(lchar_positional_prob_dict, ochar_positional_prob_dict)
        elif self.method == 'probabilistic':
            found = False
            attempt = 1
            while not found:
                guessed_word = self.heuristic_probabilistic(lchar_positional_prob_dict, ochar_positional_prob_dict, uchar_dict, lchar_dict, other_possible_char_list)
                if isinstance(guessed_word, type(None)):
                    if len(self.temp_filtered_word_list) == 1:
                        guessed_word = self.temp_filtered_word_list[0]
                        found = True
                else:
                    found = True
                self.temp_filtered_word_list = self.filtered_word_list
                print(f'Attempt {attempt} finished.')
                attempt += 1
                if attempt > 3:
                    guessed_word = random.choice(self.temp_filtered_word_list)
                    found = True
        print(f'guessed_word={guessed_word} self.guessed_word_dict={self.guessed_word_dict}')
        return guessed_word

    def get_start_word(self):
        # start_word_list = ['adieu', 'about', 'crust', 'audio', 'trace', 'crate', 'slate', 'roast', 'round', 'sound']
        # #start_word_list = ['adieu']#, 'about', 'crust', 'audio', 'trace', 'crate', 'slate', 'reast']
        # return random.choice(start_word_list)
        return "slate"

    def get_csp_guess(self, attempt_num, feedback, missing_chars):
        if attempt_num == 0:
            self.attempt_num_in_current_trial = 1
            self.filtered_word_list = self.word_list
            self.char_failed_position = dict()
            return self.get_start_word()
        else:
            self.attempt_num_in_current_trial += 1
            self.guessed_word_dict = dict()
            return self.next_guess(feedback, missing_chars)


    def play_wordle(self, target_word):
        target_word = target_word
        attempt_num = 0
        missing_chars = []

        print("Welcome to Wordle! Try to guess the 5-letter word.")
        print(
            "You have 6 attempts. Feedback uses uppercase for correct letter and position, lowercase for correct letter but wrong position, '*' for incorrect letters.")
        feedback = ''
        while attempt_num < 6:
            guess = self.get_csp_guess(attempt_num, feedback, missing_chars)
            attempt_num += 1

            if guess == target_word:
                feedback = self.calculate_feedback(guess, target_word)
                print(f"Attempt {attempt_num}: {guess} Feedback: {feedback}")
                print(f"Congratulations! You guessed the word '{target_word}' in {attempt_num} attempts.")
                self.successCount["successes"] += 1
                break

            feedback = self.calculate_feedback(guess, target_word)
            print(f"Attempt {attempt_num}: {guess} Feedback: {feedback}")

            missing_chars.extend([letter for letter in guess if letter not in target_word])
            self.print_missing_chars(missing_chars)

        if attempt_num == 6:
            print(f"Sorry, you've run out of attempts. The target word was '{target_word}'.")
            self.successCount["failures"] += 1

        if attempt_num == 1 and guess == target_word:
            self.attemptCount["tries1"] += 1
        elif attempt_num == 2 and guess == target_word:
            self.attemptCount["tries2"] += 1
        elif attempt_num == 3 and guess == target_word:
            self.attemptCount["tries3"] += 1
        elif attempt_num == 4 and guess == target_word:
            self.attemptCount["tries4"] += 1
        elif attempt_num == 5 and guess == target_word:
            self.attemptCount["tries5"] += 1
        elif attempt_num == 6 and guess == target_word:
            self.attemptCount["tries6"] += 1


    def run(self):
        print('Wordle is using '+self.wl+' as word list.')

        for i in range(self.trials):
            print(f'\nTrial {i + 1} started...')
            random_target_word = self.pick_random_target_word()
            '''random_target_word = 'loyal'
            self.get_wl()'''
            print(f'Target Word = {random_target_word}')
            self.play_wordle(random_target_word)
            print(f'Trial {i + 1} ended.')

        if self.trials > 1:
            successes = self.successCount["successes"]
            print(f'Successes: {successes}')

            # tallies of each guess amount
            oneGuess = self.attemptCount["tries1"]
            twoGuess = self.attemptCount["tries2"]
            threeGuess = self.attemptCount["tries3"]
            fourGuess = self.attemptCount["tries4"]
            fiveGuess = self.attemptCount["tries5"]
            sixGuess = self.attemptCount["tries6"]

            sumGuess = oneGuess*1 + twoGuess*2 + threeGuess*3 + fourGuess*4 + fiveGuess*5 + sixGuess*6
            avgGuess = sumGuess / successes
            print(f"First tries: {oneGuess}")
            print(f"Success Rate: {successes/self.trials: 0.3f}")
            print(f'Average Guesses: {avgGuess}')



if __name__ == "__main__":
    user_input = input("Would you like to use random or probabilistic protocol? Input 1 for random, 2 for probabilistic: ")

    # If statement to decide the protocol
    if user_input == '1':
        print("Using random protocol.")
        wdl = wordle('realWordleList.txt', 'random', trials=10000)
    elif user_input == '2':
        print("Using probabilistic protocol.")
        wdl = wordle('realWordleList.txt', 'probabilistic', trials=1)
    else:
        print("Invalid input. Please enter 1 for random or 2 for probabilistic.")

    #wdl = wordle('valid-wordle-words.txt', trials=2)
    #wdl = wordle('realWordleList.txt', 'random', trials=1)
    #wdl = wordle('realWordleList.txt', 'probabilistic', trials=1)
    #wdl = wordle('realWordleList.txt', 'random', trials=10000)
    wdl.run()
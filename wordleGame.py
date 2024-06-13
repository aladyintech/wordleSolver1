import random

def read_word_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().lower() for line in file]

def generate_target_word(word_list):
    return random.choice(word_list)

def get_user_guess():
    while True:
        guess = input("Enter your 5-letter word guess: ").strip().lower()
        if len(guess) != 5 or not guess.isalpha():
            print("Please enter a valid 5-letter word.")
        else:
            return guess


def calculate_feedback(guess, target):
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


def print_missed_letters(missed_letters):
    if missed_letters:
        print("Missed letters:")
        sorted_missed_letters = sorted(set(missed_letters))
        print(" ".join(sorted_missed_letters))
    else:
        return 0

def play_wordle(word_list):
    target_word = generate_target_word(word_list)
    attempts = 0
    missed_letters = []

    print("Welcome to Wordle! Try to guess the 5-letter word.")
    print("You have 6 attempts. Use uppercase for correct letter and position, lowercase for correct letter but wrong position, '*' for incorrect letters.")

    while attempts < 6:
        guess = get_user_guess()
        attempts += 1

        if guess == target_word:
            print(f"Congratulations! You guessed the word '{target_word}' in {attempts} attempts.")
            break

        feedback = calculate_feedback(guess, target_word)
        print(f"Attempt {attempts}: {guess} Feedback: {feedback}")
        
        missed_letters.extend([letter for letter in guess if letter not in target_word])
        print_missed_letters(missed_letters)

    if attempts == 6:
        print(f"Sorry, you've run out of attempts. The target word was '{target_word}'.")

if __name__ == "__main__":
    word_list = read_word_list("valid-wordle-words.txt")
    play_wordle(word_list)

import random

lowest_num = 1
highest_num = 100
answer = random.randint(lowest_num, highest_num)
guesses = 0
is_running = True

print("Python guessing game")
print(f"Select a number between {lowest_num} and {highest_num}")

while is_running:
    guess = input("Enter your guess: ")

    if guess.isdigit():
        guess = int(guess)
        guesses += 1  # ✅ Fix 2: track guesses

        if guess < lowest_num or guess > highest_num:
            print(f"Please enter a number between {lowest_num} and {highest_num}")  # ✅ Fix 4
        elif guess < answer:
            print("Too low, try again")
        elif guess > answer:
            print("Too high, try again")
        else:
            print(f"Correct! The answer was {answer}")
            print(f"You guessed the number in {guesses} guesses")
            is_running = False  # ✅ Fix 3: only stop on correct guess
    else:
        print("Invalid guess")
        print(f"Select a number between {lowest_num} and {highest_num}")
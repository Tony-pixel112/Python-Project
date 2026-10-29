# Quiz questions — 5 questions stored in a tuple
questions = (
    "How many elements are there in the periodic table?",
    "Which animal lays the largest eggs?",           # Fixed: added comma after closing quote
    "What is the most abundant gas in earth's atmosphere?",
    "How many bones are there in a human body?",
    "Which planet in the solar system is the hottest?"
)

# Answer options — must have exactly 5 inner tuples (one per question)
options = (
    ("A. 116", "B. 117", "C. 118", "D. 119"),
    ("A. Whale", "B. Crocodile", "C. Hippopotamus", "D. Shark"),
    ("A. Nitrogen", "B. Oxygen", "C. Carbon dioxide", "D. Argon"),  # Added missing Q3 options
    ("A. 206", "B. 207", "C. 208", "D. 209"),
    ("A. Mercury", "B. Venus", "C. Earth", "D. Jupiter")
)

# Correct answers — must be 5 entries matching the 5 questions in order
answers = ("C", "B", "A", "A", "B")

guesses = []
score = 0
questions_num = 0

for question in questions:
    print("-----------------------------")
    print(question)
    for option in options[questions_num]:
        print(option)

    guess = input("Enter your guess (A, B, C, D): ").strip().upper()  # Fixed: normalise input
    guesses.append(guess)

    if guess == answers[questions_num]:
        score += 1
        print("Correct!")
    else:
        print("Incorrect!")
        print(f"{answers[questions_num]} is the correct answer!")

    questions_num += 1

print("------------------------")
print("        Results         ")
print("------------------------")

print("Correct answers: ", end="")
for answer in answers:
    print(answer, end=" ")
print()

print("Your answers:    ", end="")
for guess in guesses:
    print(guess, end=" ")
print()

score = int(score / len(questions) * 100)
print(f"Your final score is: {score}%")
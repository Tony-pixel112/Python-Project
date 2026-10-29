# ============================================
#           PYTHON QUIZ GAME
# ============================================

# --- QUESTIONS LIST ---
# Each item in this list is one quiz question
# \n means "new line" — used to format the options nicely
questions = [
    "1. What does HTML stand for?\n   A) Hyper Text Markup Language\n   B) High Tech Modern Language\n   C) Hyper Transfer Markup Logic\n   D) Home Tool Markup Language",
    "2. Which symbol is used for comments in Python?\n   A) //\n   B) /*\n   C) #\n   D) --",
    "3. What does CSS stand for?\n   A) Computer Style Sheets\n   B) Cascading Style Sheets\n   C) Creative Style System\n   D) Coded Style Sheets",
    "4. Which of these is a Python data type?\n   A) Float\n   B) Letter\n   C) Word\n   D) Decimal",
    "5. What does '.append()' do in Python?\n   A) Removes an item from a list\n   B) Sorts a list\n   C) Adds an item to the end of a list\n   D) Counts items in a list"
]

# --- ANSWERS LIST ---
# The correct answer for each question above (in the same order)
answers = ["A", "C", "B", "A", "C"]

# --- SETUP VARIABLES ---
guesses = []      # Empty list to store all the user's answers
score = 0         # Starts at 0, increases by 1 for each correct answer
questions_num = 0 # Tracks which question we are currently on (starts at 0)

# --- WELCOME MESSAGE ---
# Just a visual header to greet the user when they start the quiz
print("------------------------")
print("      Welcome to        ")
print("       The Quiz!        ")
print("------------------------")

# --- MAIN QUIZ LOOP ---
# This loop keeps running until all questions have been answered
# len(questions) gives the total number of questions (5 in this case)
while questions_num < len(questions):

    # Print the current question
    print("\n" + questions[questions_num])

    # Ask the user to type their answer
    # .upper() converts their input to uppercase so "a" and "A" both work
    guess = input("Enter your guess (A, B, C, D): ").upper()

    # Save the user's answer to the guesses list for the results summary later
    guesses.append(guess)

    # Check if the user's answer matches the correct answer for this question
    if guess == answers[questions_num]:
        score += 1          # Add 1 to score if correct
        print("Correct!")
    else:
        print("Incorrect!")
        # Tell the user what the right answer was
        print(f"The correct answer was: {answers[questions_num]}")

    # Move to the next question by increasing the counter by 1
    questions_num += 1

# --- RESULTS SECTION ---
# This runs after all questions have been answered
print("\n------------------------")
print("        Results         ")
print("------------------------")

# Show total score out of total number of questions
print(f"Score: {score} / {len(questions)}")

# Calculate and show percentage score
# round() removes long decimal places e.g. 66.6666 becomes 67
print(f"Percentage: {round((score / len(questions)) * 100)}%")

# --- DETAILED ANSWER BREAKDOWN ---
# Loop through each question and show what the user answered vs the correct answer
print("\nYour answers vs Correct answers:")
for i in range(len(questions)):
    # Show a tick ✓ if they got it right, or a cross ✗ if they got it wrong
    status = "✓" if guesses[i] == answers[i] else "✗"
    print(f"Q{i+1}: You answered {guesses[i]} | Correct: {answers[i]} {status}")

# --- PERFORMANCE FEEDBACK ---
# Give the user a message based on how well they did
if score == len(questions):
    print("\nPerfect score! Excellent work!")
elif score >= len(questions) / 2:
    print("\nGood job! Keep practicing!")
else:
    print("\nKeep studying, you'll do better next time!")

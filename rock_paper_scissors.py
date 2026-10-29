# ============================================
#       ROCK, PAPER, SCISSORS GAME
#          Best of 5 Rounds
# ============================================

# Import random module so the computer can make random choices
import random

# The three valid game options stored in a tuple
options = ("rock", "paper", "scissors")

# --- SCORE TRACKERS ---
# These variables keep count throughout all 5 rounds
player_score = 0
computer_score = 0
draws = 0

# Welcome message shown when the game starts
print("------------------------")
print("  Rock, Paper, Scissors ")
print("    Best of 5 Rounds!   ")
print("------------------------")

# --- MAIN GAME LOOP ---
# range(1, 6) counts from 1 to 5, giving us exactly 5 rounds
for round_num in range(1, 6):
    print(f"\n--- Round {round_num} of 5 ---")

    # Computer randomly picks one of the three options
    # This happens before the player types, so it's completely fair
    computer = random.choice(options)

    # --- INPUT VALIDATION LOOP ---
    # Keeps asking until the player types a valid option
    # .lower() converts input to lowercase so "Rock" and "ROCK" both work
    # .strip() removes any accidental spaces before or after the word
    while True:
        player = input("Choose (rock, paper, scissors): ").lower().strip()
        if player in options:
            break  # Exit the loop if the input is valid
        print("Invalid choice! Please type rock, paper or scissors.")

    # Show what both the player and computer chose this round
    print(f"You chose:      {player}")
    print(f"Computer chose: {computer}")

    # --- ROUND RESULT LOGIC ---
    # Check if it's a draw (both chose the same thing)
    if player == computer:
        print("Result: Draw!")
        draws += 1

    # Check all three ways the player can win
    elif (player == "rock" and computer == "scissors") or \
         (player == "scissors" and computer == "paper") or \
         (player == "paper" and computer == "rock"):
        print("Result: You win this round!")
        player_score += 1  # Add 1 to player's score

    # If it's not a draw and not a player win, computer wins
    else:
        print("Result: Computer wins this round!")
        computer_score += 1  # Add 1 to computer's score

    # Show the running score after every round so player can track progress
    print(f"Score => You: {player_score} | Computer: {computer_score} | Draws: {draws}")

# --- FINAL RESULTS ---
# This section runs after all 5 rounds are complete
print("\n========================")
print("       FINAL RESULTS    ")
print("========================")
print(f"Your score:       {player_score}")
print(f"Computer's score: {computer_score}")
print(f"Draws:            {draws}")
print("------------------------")

# --- DECLARE OVERALL WINNER ---
# Compare final scores to decide who won the game
if player_score > computer_score:
    print("WINNER: You win the game! Well done!")
elif computer_score > player_score:
    print("WINNER: Computer wins the game! Better luck next time!")
else:
    # If scores are equal after 5 rounds, it's an overall tie
    print("OVERALL: It's a tie! Great match!")

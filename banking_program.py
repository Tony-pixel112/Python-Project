# ---------------------------------------------------------
# Simple Banking Program
# Lets a user check their balance, deposit money, or
# withdraw money, using a menu-driven loop.
# ---------------------------------------------------------

def show_balance(balance):
    """Print the current balance."""
    print(f"Your current balance is: ${balance:.2f}")


def deposit(balance):
    """
    Ask the user how much to deposit, add it to the balance,
    and return the new balance.
    """
    amount = float(input("Enter amount to deposit: $"))

    # Guard against negative or zero deposits
    if amount <= 0:
        print("Deposit amount must be positive.")
        return balance

    balance += amount
    print(f"Deposited ${amount:.2f}. New balance: ${balance:.2f}")
    return balance


def withdraw(balance):
    """
    Ask the user how much to withdraw, subtract it from the
    balance if there's enough money, and return the new balance.
    """
    amount = float(input("Enter amount to withdraw: $"))

    if amount <= 0:
        print("Withdrawal amount must be positive.")
        return balance

    # Can't withdraw more money than what's in the account
    if amount > balance:
        print("Insufficient funds.")
        return balance

    balance -= amount
    print(f"Withdrew ${amount:.2f}. New balance: ${balance:.2f}")
    return balance


# --- Main program starts here ---

b = 0  # starting balance (named 'b' so it doesn't collide with
       # any function names like "balance")
is_running = True

while is_running:
    print("\n--- Banking Menu ---")
    print("1. Show Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

    choice = input("Choose your choice (1-4): ")

    if choice == "1":
        show_balance(b)
    elif choice == "2":
        # deposit() returns the updated balance, so we
        # reassign it back to 'b' to keep it up to date
        b = deposit(b)
    elif choice == "3":
        b = withdraw(b)
    elif choice == "4":
        is_running = False
    else:
        print("Invalid choice. Please enter a number from 1 to 4.")

print("Thank you for using our banking services!")

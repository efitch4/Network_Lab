import random

def guess_the_number():
    print("Welcome to guess the number")
    print("I have choosen a number between 1 and 100 . Can you guess what it is?")

    number_to_guess = random.randint(1, 100)
    attempts = 0 
    guessed_correctly = False

    while not guessed_correctly:
        try:
            user_guess = int(input("Enter your guess?"))
            attempts += 1

            if user_guess < number_to_guess:
                print("Too low ! Try again")
            elif user_guess > number_to_guess:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
                guessed_correctly = True
        
        except ValueError:
            print("Please enter a valid number.")

# Run the game
guess_the_number()
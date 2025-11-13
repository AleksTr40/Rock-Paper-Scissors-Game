import random
import time
import json
import os

# Colours
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Secret option
secret_option = "shotgun"

# Handle draw with math quiz (includes difficulty)
def handle_draw(player_scorer, robot_scorer, difficulty):
    if difficulty == "easy":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        operations = ['+', '-']
        time_limit = 10
    elif difficulty == "medium":
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        operations = ['+', '-', '*']
        time_limit = 8
    else:  # hard
        a = random.randint(1, 50)
        b = random.randint(1, 50)
        operations = ['+', '-', '*', '/']
        time_limit = 6

    operation = random.choice(operations)
    question = f"What is {a} {operation} {b}?"

    if operation == '+':
        correct_answer = a + b
    elif operation == '-':
        correct_answer = a - b
    elif operation == '*':
        correct_answer = a * b
    else:
        correct_answer = a / b

    print("You have to solve a Math quiz")
    print("Rules are simple: solve the problem quickly to win the round.")
    print(question)
    start_time = time.time()

    try:
        player_answer = float(input("Your answer: "))
    except ValueError:
        print(RED + "That's not a number! Computer wins the round. Stupid.." + RESET)
        robot_scorer += 1
        return player_scorer, robot_scorer
    finally:
        end_time = time.time()

    time_taken = end_time - start_time

    if abs(player_answer - correct_answer) < 0.01 and time_taken <= time_limit:
        print(GREEN + "Correct and fast! You win the round. You will be a mathematician.. One day..." + RESET)
        player_scorer += 1
    else:
        print(RED + "Too slow or wrong! Computer wins the round. You are balls at Math.." + RESET)
        robot_scorer += 1

    return player_scorer, robot_scorer

# Greeting
print("Welcome to my Rock, Paper, Scissors game! ")
# Ask for player name
player_name = input("Enter your name: ")

# Load profiles
if os.path.exists("profiles.json"):
    try:
        with open("profiles.json", "r") as file:
            player_profiles = json.load(file)
    except json.JSONDecodeError:
        player_profiles = {}
else:
    player_profiles = {}
if player_name not in player_profiles:
    print("New player detected. Creating profile...")
    player_profiles[player_name] = {"total_wins": 0, "total_losses": 0}
else:
    print(f"Welcome back, {player_name}!")
    print(f"Your stats — Wins: {player_profiles[player_name]['total_wins']}, Losses: {player_profiles[player_name]['total_losses']}")

#Choosing game mode
print("Choose your game mode:")
print("1 - Classic (Rock, Paper, Scissors)")
print("2 - Extended (Rock, Paper, Scissors, Lizard, Spock)")
mode_choice = input("Enter 1 or 2: ")

if mode_choice == "2":
    options = ("rock", "paper", "scissors", "lizard", "spock")
    extended_mode = True
    print("You chose Extended mode! You like a challenge huh?")
    print("Rules:")
    print("- Rock crushes Scissors and crushes Lizard")
    print("- Paper covers Rock and disproves Spock")
    print("- Scissors cuts Paper and decapitates Lizard")
    print("- Lizard eats Paper and poisons Spock")
    print("- Spock smashes Scissors and vaporizes Rock")
else:
    options = ("rock", "paper", "scissors")
    extended_mode = False
    print("You chose Classic mode! Its a Classic!")
    print("Rules:")
    print("- Rock beats Scissors")
    print("- Paper beats Rock")
    print("- Scissors beats Paper")



# Ask for difficulty
print("Choose difficulty level:")
print("1 - Easy\n2 - Medium\n3 - Hard")
difficulty_choice = input("Enter 1, 2, or 3: ")

if difficulty_choice == "1":
    difficulty = "easy"
    win_threshold = 3
elif difficulty_choice == "2":
    difficulty = "medium"
    win_threshold = 4
elif difficulty_choice == "3":
    difficulty = "hard"
    win_threshold = 5
else:
    print("Invalid choice. Defaulting to medium.")
    difficulty = "medium"
    win_threshold = 4

# Main game loop
while True:
    player_score = 0
    robot_score = 0
    hint_shown = False

    while player_score < win_threshold and robot_score < win_threshold:
        player = input(f"Choose {', '.join(options)}: ").lower()
        robot = random.choice(options)
        print("Computer chose: " + robot)

        if player not in options and player != secret_option:
            print("There are no items like that. Try again!")
            continue

        if player == robot:
            player_score, robot_score = handle_draw(player_score, robot_score, difficulty)

        elif (
            player == "shotgun" or
            (player == "rock" and robot in ["scissors", "lizard"] if extended_mode else robot == "scissors") or
            (player == "paper" and robot in ["rock", "spock"] if extended_mode else robot == "rock") or
            (player == "scissors" and robot in ["paper", "lizard"] if extended_mode else robot == "paper") or
            (extended_mode and player == "lizard" and robot in ["spock", "paper"]) or
            (extended_mode and player == "spock" and robot in ["scissors", "rock"])
        ):
            print(GREEN + "You win this round." + RESET)
            player_score += 1

        else:
            print(RED + "Computer wins this round." + RESET)
            robot_score += 1

        print("Score — You: " + GREEN + str(player_score) + RESET + " | Computer: " + RED + str(robot_score) + RESET)


         #Secret Thingy😉
        if robot_score == win_threshold - 1 and not hint_shown:
            print(YELLOW + "Psst... there's a secret option called 'shotgun'... Try it! But be careful, you can only use it once!" + RESET)
            hint_shown = True

    if player_score == win_threshold:
        print(GREEN + "You won the game! Finally..." + RESET)
        player_profiles[player_name]["total_wins"] += 1
    else:
        print(RED + "Computer won the game! Weak!..." + RESET)
        player_profiles[player_name]["total_losses"] += 1

    print("Total stats for " + player_name + " — Wins: " + GREEN + str(player_profiles[player_name]["total_wins"]) + RESET +
          " | Losses: " + RED + str(player_profiles[player_name]["total_losses"]) + RESET)

    with open("profiles.json", "w") as file:
        json.dump(player_profiles, file, indent=4)

    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again != "yes":
        print("Thanks for playing, and go watch your meeting!")
        break
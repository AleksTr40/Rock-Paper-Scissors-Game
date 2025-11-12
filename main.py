import random
import time
import json
import os

# Colours
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Game options (replaced later by dynamic ruleset)
secret_option = "shotgun"

# ---------------------------
# Object-Oriented Engine
# ---------------------------
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Set, Tuple

class Outcome(str, Enum):
    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"

@dataclass(eq=False)
class Element:
    code: str
    name: str
    description: Optional[str] = None
    tags: Set[str] = field(default_factory=set)
    def __hash__(self): return hash(self.code)

@dataclass
class Interaction:
    source: Element
    target: Element
    outcome: Outcome
    strength: float = 1.0
    ruletext: Optional[str] = None

class RulesetBuilder:
    def __init__(self, code: str, name: str):
        self.ruleset_code = code
        self.ruleset_name = name
        self.elements: dict[str, Element] = {}
        self.interactions: dict[Tuple[str, str], Interaction] = {}

    def add_element(self, code: str, name: str) -> Element:
        el = Element(code=code, name=name)
        self.elements[code] = el
        return el

    def add_interaction(self, source: Element, target: Element, outcome: Outcome, ruletext: Optional[str] = None):
        self.interactions[(source.code, target.code)] = Interaction(source, target, outcome, ruletext=ruletext)
        reverse_outcome = Outcome.DRAW if source == target else (
            Outcome.LOSE if outcome == Outcome.WIN else Outcome.WIN
        )
        self.interactions[(target.code, source.code)] = Interaction(target, source, reverse_outcome)

    def decide(self, a: Element, b: Element) -> Tuple[Outcome, Optional[str]]:
        inter = self.interactions.get((a.code, b.code))
        if inter:
            return inter.outcome, inter.ruletext
        return Outcome.DRAW, None

# ---------------------------
# Setup Ruleset
# ---------------------------
builder = RulesetBuilder("rps", "Rock Paper Scissors")
rock = builder.add_element("rock", "Rock")
paper = builder.add_element("paper", "Paper")
scissors = builder.add_element("scissors", "Scissors")
builder.add_interaction(rock, scissors, Outcome.WIN, "Rock crushes scissors")
builder.add_interaction(scissors, paper, Outcome.WIN, "Scissors cuts paper")
builder.add_interaction(paper, rock, Outcome.WIN, "Paper covers rock")
options = list(builder.elements.keys())  # dynamic options

# Handle draw with math quiz
def handle_draw(player_scorer, robot_scorer):
    a = random.randint(1, 12)
    b = random.randint(1, 12)
    operation = random.choice(['+', '-', '*'])
    question = f"What is {a} {operation} {b}?"

    if operation == '+':
        correct_answer = a + b
    elif operation == '-':
        correct_answer = a - b
    else:
        correct_answer = a * b

    print("You have to solve a Math quiz")
    print("Rules are simple: solve the problem quickly to win the round. If you're slow or wrong, the computer wins.")
    print("I hope you are good at Math... You should..")
    print(question)
    start_time = time.time()

    try:
        player_answer = int(input("Your answer: "))
    except ValueError:
        print(RED + "That's not a number! Computer wins the round. That's terrible.." + RESET)
        robot_scorer += 1
        return player_scorer, robot_scorer
    finally:
        end_time = time.time()

    time_taken = end_time - start_time

    if player_answer == correct_answer and time_taken <= 8:
        print(GREEN + "Correct and fast! You win the round. You will be a mathematician.." + RESET)
        player_scorer += 1
    else:
        print(RED + "Too Slow or Wrong Answer! Computer wins the round. U suck at Math.." + RESET)
        robot_scorer += 1

    return player_scorer, robot_scorer

# Greeting
print("Welcome to my Rock, Paper, Scissors MVP!")
print("This game will make you less bored!")
print("Rock beats scissors, scissors beats paper, paper beats rock.")
print("First to 3 points wins.")

# Load profiles
if os.path.exists("profiles.json"):
    try:
        with open("profiles.json", "r") as file:
            player_profiles = json.load(file)
    except json.JSONDecodeError:
        player_profiles = {}
else:
    player_profiles = {}

# Ask for player name
player_name = input("Enter your name: ")

if player_name not in player_profiles:
    print("New player detected. Creating profile...")
    player_profiles[player_name] = {"total_wins": 0, "total_losses": 0}
else:
    print(f"Welcome back, {player_name}!")
    print(f"Your stats — Wins: {player_profiles[player_name]['total_wins']}, Losses: {player_profiles[player_name]['total_losses']}")

# Main game loop
while True:
    player_score = 0
    robot_score = 0
    hint_shown = False

    while player_score < 3 and robot_score < 3:
        player = input("Choose rock, paper, or scissors: ").lower()
        robot = random.choice(options)
        print("Computer chose: " + robot)

        if player not in options and player != secret_option:
            print("There are no items like that. Try again!")
            continue

        if player == robot:
            player_score, robot_score = handle_draw(player_score, robot_score)

        elif player == secret_option:
            print(GREEN + "You win this round." + RESET)
            player_score += 1

        else:
            player_element = builder.elements[player]
            robot_element = builder.elements[robot]
            outcome, ruletext = builder.decide(player_element, robot_element)

            if outcome == Outcome.WIN:
                print(GREEN + "You win this round." + RESET)
                player_score += 1
            elif outcome == Outcome.LOSE:
                print(RED + "Computer wins this round." + RESET)
                robot_score += 1
            else:
                player_score, robot_score = handle_draw(player_score, robot_score)

        print("Score — You: " + GREEN + str(player_score) + RESET + " | Computer: " + RED + str(robot_score) + RESET)

        if robot_score == 2 and not hint_shown:
            print(YELLOW + "Psst... there's a secret option called 'shotgun'... Try it! But be careful, you can only use it once!" + RESET)
            hint_shown = True

    if player_score == 3:
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
        print("Thanks for playing, and watch your meeting!")
        break

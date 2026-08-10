# This file will contain the application logic and menu with multiple card games

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS AND HELPER FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from managers import BlackjackManager, GoFishManager


def gameMenu():
    validChoice = False
    while not validChoice:
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")
        print("                     CARD GAMES")
        print("")
        print("                     1. Blackjack")
        print("                     2. Go Fish")
        print("                     3. Exit")
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")
        print("Which game would you like to play?")
        choice = input(" --> ").lower()

        if choice in ["1", "blackjack", "b"]:
            choice = "blackjack"
            validChoice = True
        elif choice in ["2", "go fish", "gofish", "g"]:
            choice = "go fish"
            validChoice = True
        elif choice in ["3", "exit", "quit", "q"]:
            choice = "exit"
            validChoice = True
        else:
            print("")
            print("Invalid choice - please choose again!")

    return choice


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN FUNCTION DEFINITION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    running = True
    while running:
        gameChoice = gameMenu()

        if gameChoice == "blackjack":
            blackjackGame = BlackjackManager()
            blackjackGame.playGame()
        elif gameChoice == "go fish":
            goFishGame = GoFishManager()
            goFishGame.playGame()
        else:
            running = False

    print("")
    print("Thanks for playing!")




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN FUNCTION CALL
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
main()

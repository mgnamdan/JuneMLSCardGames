# This file will contain the class definitions for the game manager objects
from players import CompBlackjackPlayer, HumanBlackjackPlayer
from decks import NormalDeck
from random import choice, randint


class BlackjackManager:

    COMPNAMES = ["Alex", "Becky", "Charlie", "Devyn", "Eric", "Francine", "Gus", "Hannah"]

    def __init__(self):
        self.playGame()


    def reset(self):
        self.deck = NormalDeck()
        self.dealer = CompBlackjackPlayer()
        self.players = []

        for _ in range(randint(3, 5)):
            self.deck.shuffle()

        print("")
        print("Enter your name:")
        humName = input(" --> ")
        humanPlayer = HumanBlackjackPlayer(humName)
        self.players.append(humanPlayer)

        print("")
        print("How many computers would you like to play against? (1-4)")
        numComps = input(" --> ")

        try:
            numComps = int(numComps)
            if numComps < 1:
                numComps = 1
            if numComps > 4:
                numComps = 4
            numComps -= 1
        except ValueError:
            numComps = 0

        usedNames = []
        for _ in range(numComps):
            validName = False
            while not validName:
                compName = choice(self.COMPNAMES)
                if compName not in usedNames:
                    compPlayer = CompBlackjackPlayer(compName)
                    self.players.append(compPlayer)
                    validName = True

        self.players.append(self.dealer)

        for _ in range(2):
            for player in self.players:
                player.drawCard(self.deck.draw())


    def manageTurn(self, player):
        keepGoing = True
        while keepGoing:
            playerChoice = player.makeChoice()
            if playerChoice == "hit":
                player.drawCard(self.deck.draw())
            else:
                keepGoing = False


    def determineWinner(self):
        scores = {}
        for player in self.players:
            pScore = player.giveScore()
            if pScore in scores.keys():
                scores[pScore].append(player)
            elif pScore <= 21:
                scores[pScore] = [player]
            else:
                continue

        highScore = max(scores.keys())
        winners = scores[highScore]

        if len(winners) == 0:
            print("")
            print("Nobody wins - everyone busted!")
        elif len(winners) == 1:
            print(f"{winners[0]} wins with a score of {highScore}!")
        else:
            if self.dealer in winners:
                print(f"The {self.dealer} wins with a score of {highScore}")
            else:
                for idx in range(len(winners)):
                    message = ""
                    if idx == len(winners) - 1:
                        message += f" and {winners[idx]} win with a score of {highScore}!"
                    else:
                        message += f"{winners[idx]}, "


    def promptNextGame(self):
        validChoice = False
        while not validChoice:
            print("")
            print("Would you like to play again? (y/n)")
            choice = input(" --> ").lower()
            if choice in ["yes", "y"]:
                choice = True
                validChoice = True
            elif choice in ["no", "n", "exit", "quit"]:
                choice = False
                validChoice = True
            else:
                print("")
                print("Invalid choice - please choose again!")
        return choice


    def playGame(self):
        playing = True
        while playing:
            self.reset()
            for player in self.players:
                self.manageTurn(player)
            self.determineWinner()
            playing = self.promptNextGame()
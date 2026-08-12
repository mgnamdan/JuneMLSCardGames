# This file will contain the class definitions for the game manager objects
from players import CompBlackjackPlayer, HumanBlackjackPlayer, GoFishCompPlayer, GoFishHumanPlayer
from decks import NormalDeck
from currency import Currency
from random import choice, randint


class BlackjackManager:

    COMPNAMES = ["Alex", "Becky", "Charlie", "Devyn", "Eric", "Francine", "Gus", "Hannah"]


    def __init__(self):
        self.chips = Currency(10, "USD")
        self.currentBet = Currency(0, "USD")


    def reset(self):
        self.deck = NormalDeck()
        self.dealer = CompBlackjackPlayer()
        self.players = []
        self.currentBet = Currency(0, "USD")

        for _ in range(randint(3, 5)):
            self.deck.shuffle()

        print("")
        print("Enter your name:")
        humName = input(" --> ")
        humanPlayer = HumanBlackjackPlayer(humName)
        humanPlayer.chips = self.chips
        self.players.append(humanPlayer)

        print("")
        print("How many total players would you like? (2-4)")
        numPlayers = input(" --> ")

        try:
            numPlayers = int(numPlayers)
            if numPlayers < 2:
                numPlayers = 2
            if numPlayers > 4:
                numPlayers = 4
            numComps = numPlayers - 2
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
                    usedNames.append(compName)
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


    def formatCurrency(self, currency):
        return f"${currency.amount:.2f} {currency.denomination}"


    def placeBet(self, betAmount):
        betAmount = round(float(betAmount), 2)
        maxBet = min(2.0, self.chips.amount)
        if betAmount < 0 or betAmount > maxBet:
            raise ValueError(f"Bet must be between $0.00 and ${maxBet:.2f}.")

        self.currentBet = Currency(betAmount, self.chips.denomination)
        self.chips -= betAmount


    def promptBet(self):
        maxBet = min(2.0, self.chips.amount)
        validBet = False
        while not validBet:
            print("")
            print(f"You have {self.formatCurrency(self.chips)} in chips.")
            print(f"How much would you like to bet? ($0.00-${maxBet:.2f})")
            betChoice = input(" --> ").replace("$", "")

            try:
                self.placeBet(betChoice)
                validBet = True
            except ValueError:
                print("")
                print(f"Invalid bet - choose an amount from $0.00 to ${maxBet:.2f}!")

        print(f"Bet placed: {self.formatCurrency(self.currentBet)}")


    def getWinnerInfo(self):
        scores = {}
        for player in self.players:
            pScore = player.giveScore()
            if pScore in scores.keys():
                scores[pScore].append(player)
            elif pScore <= 21:
                scores[pScore] = [player]
            else:
                continue

        if len(scores) == 0:
            return None, []

        highScore = max(scores.keys())
        winners = scores[highScore]
        return highScore, winners


    def determineWinner(self):
        highScore, winners = self.getWinnerInfo()

        if len(winners) == 0:
            print("")
            print("Nobody wins - everyone busted!")
        elif len(winners) == 1:
            print(f"{winners[0]} wins with a score of {highScore}!")
        else:
            if self.dealer in winners:
                print(f"The {self.dealer} wins with a score of {highScore}")
            else:
                message = ""
                for idx in range(len(winners)):
                    if idx == len(winners) - 1:
                        message += f"and {winners[idx]} win with a score of {highScore}!"
                    else:
                        message += f"{winners[idx]}, "
                print(message)
        return winners


    def settleBet(self, winners):
        humanPlayer = self.players[0]
        betAmount = self.currentBet.amount

        if betAmount == 0:
            result = "No chips were wagered."
        elif len(winners) == 1 and humanPlayer in winners:
            self.chips += betAmount * 2
            result = f"You won {self.formatCurrency(Currency(betAmount * 2))}!"
        elif humanPlayer in winners and self.dealer not in winners:
            self.chips += betAmount
            result = "The game was tied, so your bet was returned."
        else:
            result = f"You lost your {self.formatCurrency(self.currentBet)} bet."

        print("")
        print(result)
        print(f"Chip balance: {self.formatCurrency(self.chips)}")


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
            self.manageTurn(self.players[0])
            self.promptBet()
            for player in self.players[1:]:
                self.manageTurn(player)
            winners = self.determineWinner()
            self.settleBet(winners)
            playing = self.promptNextGame()




class GoFishManager:

    COMPNAMES = ["Alex", "Becky", "Charlie", "Devyn", "Eric", "Francine", "Gus", "Hannah"]


    def reset(self):
        self.deck = NormalDeck()
        self.players = []

        for _ in range(randint(3, 5)):
            self.deck.shuffle()

        print("")
        print("Enter your name:")
        humName = input(" --> ")
        humanPlayer = GoFishHumanPlayer(humName)
        self.players.append(humanPlayer)

        print("")
        print("How many total players would you like? (2-4)")
        numPlayers = input(" --> ")

        try:
            numPlayers = int(numPlayers)
            if numPlayers < 2:
                numPlayers = 2
            if numPlayers > 4:
                numPlayers = 4
        except ValueError:
            numPlayers = 2

        usedNames = [humName]
        numComps = numPlayers - 1
        for _ in range(numComps):
            validName = False
            while not validName:
                compName = choice(self.COMPNAMES)
                if compName not in usedNames:
                    compPlayer = GoFishCompPlayer(compName)
                    self.players.append(compPlayer)
                    usedNames.append(compName)
                    validName = True

        for player in self.players:
            player.memoryLimit = len(self.players) + 1

        if len(self.players) == 2:
            numCards = 7
        else:
            numCards = 5

        for _ in range(numCards):
            for player in self.players:
                player.drawCard(self.deck.draw())

        for player in self.players:
            self.checkPlayerPairs(player)


    def getComputerPlayers(self):
        computerPlayers = []
        for player in self.players:
            if isinstance(player, GoFishCompPlayer) and not isinstance(player, GoFishHumanPlayer):
                computerPlayers.append(player)
        return computerPlayers


    def rememberRequest(self, askingPlayer, requestedRank):
        computerPlayers = self.getComputerPlayers()
        for computer in computerPlayers:
            computer.rememberRequest(askingPlayer, requestedRank)


    def forgetCard(self, player, rank):
        computerPlayers = self.getComputerPlayers()
        for computer in computerPlayers:
            computer.forgetCard(player, rank)


    def checkPlayerPairs(self, player):
        newPairs = player.checkForPairs()
        for newPair in newPairs:
            pairRank = newPair[0].rank
            print(f"{player} made a pair of {pairRank} cards!")
            self.forgetCard(player, pairRank)
        return newPairs


    def gameIsOver(self):
        if len(self.deck.drawPile) == 0:
            return True

        for player in self.players:
            if len(player.hand) == 0:
                return True

        return False


    def manageTurn(self, player):
        keepGoing = True
        while keepGoing and not self.gameIsOver():
            print("")
            print(f"~~~~~~~~~~~~~~~~~~~~ {player.name.upper()}'S TURN ~~~~~~~~~~~~~~~~~~~~")
            askedPlayer, requestedRank = player.makeChoice(self.players)

            if askedPlayer is None or requestedRank is None:
                return

            print("")
            print(f"{player} asks {askedPlayer} for {requestedRank} cards.")
            self.rememberRequest(player, requestedRank)
            givenCards = askedPlayer.giveCards(requestedRank)

            if len(givenCards) > 0:
                print(f"{askedPlayer} gives {player} {len(givenCards)} card(s).")
                self.forgetCard(askedPlayer, requestedRank)
                for card in givenCards:
                    player.drawCard(card)
                self.checkPlayerPairs(player)
                keepGoing = True
            else:
                print(f"{askedPlayer} says, 'Go Fish!'")
                self.forgetCard(askedPlayer, requestedRank)
                drawnCard = self.deck.draw()
                player.drawCard(drawnCard)

                if isinstance(player, GoFishHumanPlayer):
                    print(f"You drew the {drawnCard}.")
                else:
                    print(f"{player} draws a card.")

                self.checkPlayerPairs(player)
                if drawnCard.rank == requestedRank and not self.gameIsOver():
                    print(f"{player} drew the requested rank and gets another turn!")
                    keepGoing = True
                else:
                    keepGoing = False


    def determineWinner(self):
        print("")
        print("~~~~~~~~~~~~~~~~~~~~ FINAL PAIRS ~~~~~~~~~~~~~~~~~~~~")
        scores = {}
        for player in self.players:
            pScore = player.giveScore()
            if pScore == 1:
                pairWord = "pair"
            else:
                pairWord = "pairs"
            print(f"{player}: {pScore} {pairWord}")

            if pScore in scores.keys():
                scores[pScore].append(player)
            else:
                scores[pScore] = [player]

        highScore = max(scores.keys())
        winners = scores[highScore]
        if highScore == 1:
            pairWord = "pair"
        else:
            pairWord = "pairs"

        print("")
        if len(winners) == 1:
            print(f"{winners[0]} wins with {highScore} {pairWord}!")
        else:
            message = ""
            for idx in range(len(winners)):
                if idx == len(winners) - 1:
                    message += f"and {winners[idx]} tie with {highScore} {pairWord}!"
                else:
                    message += f"{winners[idx]}, "
            print(message)


    def promptNextGame(self):
        validChoice = False
        while not validChoice:
            print("")
            print("Would you like to play Go Fish again? (y/n)")
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
            currentPlayerIdx = 0

            while not self.gameIsOver():
                currentPlayer = self.players[currentPlayerIdx]
                self.manageTurn(currentPlayer)
                currentPlayerIdx += 1
                if currentPlayerIdx >= len(self.players):
                    currentPlayerIdx = 0

            print("")
            if len(self.deck.drawPile) == 0:
                print("The draw pile is empty - game over!")
            else:
                for player in self.players:
                    if len(player.hand) == 0:
                        print(f"{player} is out of cards - game over!")
                        break

            self.determineWinner()
            playing = self.promptNextGame()

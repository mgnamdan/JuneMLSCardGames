# This file will contain the class definitions for the visual game managers
from players import CompBlackjackPlayer, HumanBlackjackPlayer, GoFishCompPlayer, GoFishHumanPlayer
from decks import NormalDeck
from currency import Currency
from random import choice, randint


class BlackjackManager:

    COMPNAMES = ["Alex", "Becky", "Charlie", "Devyn", "Eric", "Francine", "Gus", "Hannah"]

    def __init__(self):
        self.finished = False
        self.chips = Currency(10, "USD")
        self.currentBet = Currency(0, "USD")
        self.settlementMessage = ""


    def startSession(self):
        self.chips = Currency(10, "USD")
        self.currentBet = Currency(0, "USD")
        self.settlementMessage = ""


    def reset(self, humName="Player", numPlayers=2):
        self.deck = NormalDeck()
        self.dealer = CompBlackjackPlayer()
        self.players = []
        self.finished = False
        self.currentBet = Currency(0, self.chips.denomination)
        self.settlementMessage = ""

        for _ in range(randint(3, 5)):
            self.deck.shuffle()

        humanPlayer = HumanBlackjackPlayer(humName)
        humanPlayer.chips = self.chips
        self.players.append(humanPlayer)
        self.humanPlayer = humanPlayer

        if numPlayers < 2:
            numPlayers = 2
        if numPlayers > 4:
            numPlayers = 4

        numComps = numPlayers - 2
        usedNames = [humName.lower()]
        for _ in range(numComps):
            validName = False
            while not validName:
                compName = choice(self.COMPNAMES)
                if compName.lower() not in usedNames:
                    compPlayer = CompBlackjackPlayer(compName)
                    self.players.append(compPlayer)
                    usedNames.append(compName.lower())
                    validName = True

        self.players.append(self.dealer)

        for _ in range(2):
            for player in self.players:
                player.drawCard(self.deck.draw())


    def hitHuman(self):
        if self.finished:
            return None
        drawnCard = self.deck.draw()
        self.humanPlayer.drawCard(drawnCard)
        return drawnCard


    def humanTurnIsOver(self):
        humanScore = self.humanPlayer.giveScore()
        return humanScore >= 21 or len(self.humanPlayer.hand) >= 5


    def completeComputerTurns(self):
        for player in self.players[1:]:
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


    def completeGame(self, betAmount=0):
        if not self.finished:
            self.placeBet(betAmount)
            self.completeComputerTurns()
            self.finished = True
            winners = self.getWinnerInfo()[1]
            self.settlementMessage = self.settleBet(winners)
        return f"{self.determineWinner()} {self.settlementMessage}"


    def getWinnerInfo(self):
        scores = {}
        for player in self.players:
            pScore = player.giveScore()
            if pScore in scores.keys():
                scores[pScore].append(player)
            elif pScore <= 21:
                scores[pScore] = [player]

        if len(scores) == 0:
            return None, []

        highScore = max(scores.keys())
        winners = scores[highScore]
        return highScore, winners


    def determineWinner(self):
        highScore, winners = self.getWinnerInfo()

        if len(winners) == 0:
            return "Nobody wins - everyone busted!"

        if len(winners) == 1:
            return f"{winners[0]} wins with a score of {highScore}!"
        elif self.dealer in winners:
            return f"The {self.dealer} wins the tie with a score of {highScore}!"
        else:
            winnerNames = []
            for winner in winners:
                winnerNames.append(str(winner))
            if len(winnerNames) == 2:
                names = f"{winnerNames[0]} and {winnerNames[1]}"
            else:
                names = ", ".join(winnerNames[:-1]) + f", and {winnerNames[-1]}"
            return f"{names} tie with a score of {highScore}!"


    def settleBet(self, winners):
        betAmount = self.currentBet.amount

        if betAmount == 0:
            result = "No chips were wagered."
        elif len(winners) == 1 and self.humanPlayer in winners:
            self.chips += betAmount * 2
            result = f"You won {self.formatCurrency(Currency(betAmount * 2))}!"
        elif self.humanPlayer in winners and self.dealer not in winners:
            self.chips += betAmount
            result = "The game was tied, so your bet was returned."
        else:
            result = f"You lost your {self.formatCurrency(self.currentBet)} bet."

        return f"{result} Balance: {self.formatCurrency(self.chips)}."




class GoFishManager:

    COMPNAMES = ["Alex", "Becky", "Charlie", "Devyn", "Eric", "Francine", "Gus", "Hannah"]

    def __init__(self):
        self.finished = False


    def reset(self, humName="Player", numPlayers=2):
        self.deck = NormalDeck()
        self.players = []
        self.currentPlayerIdx = 0
        self.finished = False
        self.openingMessages = []

        for _ in range(randint(3, 5)):
            self.deck.shuffle()

        humanPlayer = GoFishHumanPlayer(humName)
        self.players.append(humanPlayer)
        self.humanPlayer = humanPlayer

        if numPlayers < 2:
            numPlayers = 2
        if numPlayers > 4:
            numPlayers = 4

        usedNames = [humName.lower()]
        numComps = numPlayers - 1
        for _ in range(numComps):
            validName = False
            while not validName:
                compName = choice(self.COMPNAMES)
                if compName.lower() not in usedNames:
                    compPlayer = GoFishCompPlayer(compName)
                    self.players.append(compPlayer)
                    usedNames.append(compName.lower())
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
            self.openingMessages.extend(self.checkPlayerPairs(player))


    def getComputerPlayers(self):
        computerPlayers = []
        for player in self.players:
            if isinstance(player, GoFishCompPlayer) and not isinstance(player, GoFishHumanPlayer):
                computerPlayers.append(player)
        return computerPlayers


    def rememberRequest(self, askingPlayer, requestedRank):
        for computer in self.getComputerPlayers():
            computer.rememberRequest(askingPlayer, requestedRank)


    def forgetCard(self, player, rank):
        for computer in self.getComputerPlayers():
            computer.forgetCard(player, rank)


    def checkPlayerPairs(self, player):
        messages = []
        newPairs = player.checkForPairs()
        for newPair in newPairs:
            pairRank = newPair[0].rank
            messages.append(f"{player} made a pair of {pairRank} cards!")
            self.forgetCard(player, pairRank)
        return messages


    def gameIsOver(self):
        if len(self.deck.drawPile) == 0:
            return True

        for player in self.players:
            if len(player.hand) == 0:
                return True

        return False


    def giveEndReason(self):
        if len(self.deck.drawPile) == 0:
            return "The draw pile is empty - game over!"

        for player in self.players:
            if len(player.hand) == 0:
                return f"{player} is out of cards - game over!"

        return "Game over!"


    def giveCurrentPlayer(self):
        return self.players[self.currentPlayerIdx]


    def advanceTurn(self):
        self.currentPlayerIdx += 1
        if self.currentPlayerIdx >= len(self.players):
            self.currentPlayerIdx = 0


    def performRequest(self, askingPlayer, askedPlayer, requestedRank):
        messages = []
        drawnCard = None

        if self.finished or self.gameIsOver():
            self.finished = True
            return {"messages": [self.giveEndReason()], "drawnCard": None,
                    "extraTurn": False, "gameOver": True}

        messages.append(f"{askingPlayer} asks {askedPlayer} for {requestedRank} cards.")
        self.rememberRequest(askingPlayer, requestedRank)
        givenCards = askedPlayer.giveCards(requestedRank)

        if len(givenCards) > 0:
            messages.append(f"{askedPlayer} gives {askingPlayer} {len(givenCards)} card(s).")
            self.forgetCard(askedPlayer, requestedRank)
            for card in givenCards:
                askingPlayer.drawCard(card)
            messages.extend(self.checkPlayerPairs(askingPlayer))
            extraTurn = True
        else:
            messages.append(f"{askedPlayer} says, 'Go Fish!'")
            self.forgetCard(askedPlayer, requestedRank)
            drawnCard = self.deck.draw()
            askingPlayer.drawCard(drawnCard)
            messages.append(f"{askingPlayer} draws a card.")
            messages.extend(self.checkPlayerPairs(askingPlayer))
            extraTurn = drawnCard.rank == requestedRank

        if self.gameIsOver():
            self.finished = True
            extraTurn = False
            messages.append(self.giveEndReason())
        elif extraTurn:
            messages.append(f"{askingPlayer} gets another turn!")
        else:
            self.advanceTurn()

        return {"messages": messages, "drawnCard": drawnCard,
                "extraTurn": extraTurn, "gameOver": self.finished}


    def computerAction(self):
        computer = self.giveCurrentPlayer()
        askedPlayer, requestedRank = computer.makeChoice(self.players)

        if askedPlayer is None or requestedRank is None:
            self.finished = True
            return {"messages": [self.giveEndReason()], "drawnCard": None,
                    "extraTurn": False, "gameOver": True}

        return self.performRequest(computer, askedPlayer, requestedRank)


    def determineWinner(self):
        scores = {}
        scoreList = []
        for player in self.players:
            pScore = player.giveScore()
            scoreList.append((player, pScore))
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

        if len(winners) == 1:
            message = f"{winners[0]} wins with {highScore} {pairWord}!"
        else:
            winnerNames = []
            for winner in winners:
                winnerNames.append(str(winner))
            if len(winnerNames) == 2:
                names = f"{winnerNames[0]} and {winnerNames[1]}"
            else:
                names = ", ".join(winnerNames[:-1]) + f", and {winnerNames[-1]}"
            message = f"{names} tie with {highScore} {pairWord}!"

        return message, scoreList

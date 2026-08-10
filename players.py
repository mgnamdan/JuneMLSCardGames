# This file will contain the class definitions for the human and computer players
from random import choice, randint


class CompBlackjackPlayer:

    CARDVALUES = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7,
                  "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 10, "Queen":10, "King": 10, "Ace": 11}

    def __init__(self, name="Dealer"):
        self.name = name
        self.hand = []
        self.score = 0


    def __repr__(self):
        return f"{self.name}"


    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if other.name != self.name:
            return False
        if len(other.hand) != len(self.hand):
            return False
        for idx in range(len(self.hand)):
            if other.hand[idx] != self.hand[idx]:
                return False
        return True


    def drawCard(self, drawnCard):
        self.hand.append(drawnCard)


    def discardCard(self, cardIdx=0):
        return self.hand.pop(cardIdx)


    def showHand(self):
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")
        print(f"                {self.name.upper()}'S HAND")
        print("")
        if len(self.hand) == 0:
            print("                     Hand is empty!")
        else:
            print("                     1. ??? of ???")
            for idx in range(1, len(self.hand)):
                print(f"                     {idx+1}. {self.hand[idx]}")
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")


    def calcScore(self):
        self.score = 0
        aces = 0
        for card in self.hand:
            if card.rank == "Ace":
                aces += 1
            self.score += self.CARDVALUES[card.rank]

        while self.score > 21 and aces > 0:
            self.score -= 10
            aces -= 1


    def giveScore(self):
        self.calcScore()
        return self.score


    def makeChoice(self):
        self.calcScore()
        if self.score > 16 or len(self.hand) >= 5:
            return "stay"
        else:
            return "hit"




class HumanBlackjackPlayer(CompBlackjackPlayer):

    def showHand(self):
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")
        print(f"                {self.name.upper()}'S HAND")
        print("")
        if len(self.hand) == 0:
            print("                     Hand is empty!")
        else:
            for idx in range(len(self.hand)):
                print(f"                     {idx+1}. {self.hand[idx]}")
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")


    def makeChoice(self):
        validChoice = False
        while not validChoice:
            self.calcScore()
            if self.score >= 21 or len(self.hand) >= 5:
                choice = "stay"
                validChoice = True
            else:
                self.showHand()
                print("Would you like to [hit] or [stay]?")
                choice = input(" --> ").lower()
                if choice in ["hit", "h"]:
                    choice = "hit"
                    validChoice = True
                elif choice in ["stay", "s"]:
                    choice = "stay"
                    validChoice = True
                else:
                    print("")
                    print("Invalid choice - choose again!")
        return choice




class GoFishCompPlayer:

    MEMORYLIMIT = 3
    NOTICECHANCE = 75
    USEMEMORYCHANCE = 80
    FORGETCHANCE = 15

    def __init__(self, name="Computer"):
        self.name = name
        self.hand = []
        self.pairs = []
        self.memory = []
        self.memoryLimit = self.MEMORYLIMIT


    def __repr__(self):
        return f"{self.name}"


    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if other.name != self.name:
            return False
        if len(other.hand) != len(self.hand):
            return False
        for idx in range(len(self.hand)):
            if other.hand[idx] != self.hand[idx]:
                return False
        return True


    def drawCard(self, drawnCard):
        self.hand.append(drawnCard)


    def giveCards(self, requestedRank):
        cardsToGive = []
        for card in self.hand:
            if card.rank == requestedRank:
                cardsToGive.append(card)

        for card in cardsToGive:
            self.hand.remove(card)

        return cardsToGive


    def giveRanks(self):
        ranks = []
        for card in self.hand:
            if card.rank not in ranks:
                ranks.append(card.rank)
        return ranks


    def checkForPairs(self):
        newPairs = []
        ranks = self.giveRanks()

        for rank in ranks:
            matchingCards = []
            for card in self.hand:
                if card.rank == rank:
                    matchingCards.append(card)

            while len(matchingCards) >= 2:
                firstCard = matchingCards.pop(0)
                secondCard = matchingCards.pop(0)
                self.hand.remove(firstCard)
                self.hand.remove(secondCard)
                newPair = [firstCard, secondCard]
                self.pairs.append(newPair)
                newPairs.append(newPair)

        return newPairs


    def giveScore(self):
        return len(self.pairs)


    def showHand(self):
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")
        print(f"                {self.name.upper()}'S HAND")
        print("")
        if len(self.hand) == 0:
            print("                     Hand is empty!")
        else:
            for idx in range(len(self.hand)):
                print(f"                     {idx+1}. ??? of ???")
        print("")
        print(f"                     Pairs: {len(self.pairs)}")
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")


    def rememberRequest(self, askingPlayer, requestedRank):
        if askingPlayer == self:
            return
        if randint(1, 100) > self.NOTICECHANCE:
            return

        for memory in self.memory:
            if memory["player"] == askingPlayer and memory["rank"] == requestedRank:
                memory["confidence"] = 3
                return

        newMemory = {"player": askingPlayer, "rank": requestedRank, "confidence": 3}

        if len(self.memory) >= self.memoryLimit:
            lowestConfidence = min([memory["confidence"] for memory in self.memory])
            weakestMemories = []
            for memory in self.memory:
                if memory["confidence"] == lowestConfidence:
                    weakestMemories.append(memory)
            forgottenMemory = choice(weakestMemories)
            self.memory.remove(forgottenMemory)

        self.memory.append(newMemory)


    def forgetCard(self, player, rank):
        memoriesToForget = []
        for memory in self.memory:
            if memory["player"] == player and memory["rank"] == rank:
                memoriesToForget.append(memory)

        for memory in memoriesToForget:
            self.memory.remove(memory)


    def updateMemory(self, players):
        memoriesToForget = []
        for memory in self.memory:
            if memory["player"] not in players or len(memory["player"].hand) == 0:
                memoriesToForget.append(memory)
            elif randint(1, 100) <= self.FORGETCHANCE:
                memory["confidence"] -= 1
                if memory["confidence"] <= 0:
                    memoriesToForget.append(memory)

        for memory in memoriesToForget:
            self.memory.remove(memory)


    def makeChoice(self, players):
        self.updateMemory(players)
        opponents = []
        for player in players:
            if player != self and len(player.hand) > 0:
                opponents.append(player)

        if len(self.hand) == 0 or len(opponents) == 0:
            return None, None

        ranks = self.giveRanks()
        usefulMemories = []
        for memory in self.memory:
            if memory["player"] in opponents and memory["rank"] in ranks:
                usefulMemories.append(memory)

        useMemoryChance = self.USEMEMORYCHANCE
        if len(self.hand) == 1:
            highScore = max([player.giveScore() for player in players])
            if self.giveScore() + 1 >= highScore:
                useMemoryChance = 95
            else:
                useMemoryChance = 40

        if len(usefulMemories) > 0 and randint(1, 100) <= useMemoryChance:
            highestConfidence = max([memory["confidence"] for memory in usefulMemories])
            bestMemories = []
            for memory in usefulMemories:
                if memory["confidence"] == highestConfidence:
                    bestMemories.append(memory)
            selectedMemory = choice(bestMemories)
            askedPlayer = selectedMemory["player"]
            requestedRank = selectedMemory["rank"]
        else:
            askedPlayer = choice(opponents)
            requestedRank = choice(ranks)

        return askedPlayer, requestedRank




class GoFishHumanPlayer(GoFishCompPlayer):

    def showHand(self):
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")
        print(f"                {self.name.upper()}'S HAND")
        print("")
        if len(self.hand) == 0:
            print("                     Hand is empty!")
        else:
            for idx in range(len(self.hand)):
                print(f"                     {idx+1}. {self.hand[idx]}")
        print("")
        print(f"                     Pairs: {len(self.pairs)}")
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")


    def makeChoice(self, players):
        self.showHand()
        opponents = []
        for player in players:
            if player != self and len(player.hand) > 0:
                opponents.append(player)

        if len(self.hand) == 0 or len(opponents) == 0:
            return None, None

        if len(opponents) == 1:
            askedPlayer = opponents[0]
            numCards = len(askedPlayer.hand)
            numPairs = askedPlayer.giveScore()
            if numPairs == 1:
                pairWord = "pair"
            else:
                pairWord = "pairs"
            print(f"You are asking {askedPlayer} ({numCards} cards, {numPairs} {pairWord}).")
        else:
            validPlayer = False
            while not validPlayer:
                print("Who would you like to ask?")
                for idx in range(len(opponents)):
                    numCards = len(opponents[idx].hand)
                    numPairs = opponents[idx].giveScore()
                    if numPairs == 1:
                        pairWord = "pair"
                    else:
                        pairWord = "pairs"
                    print(f"  {idx+1}. {opponents[idx]} ({numCards} cards, {numPairs} {pairWord})")
                playerChoice = input(" --> ")

                try:
                    playerIdx = int(playerChoice) - 1
                    if playerIdx >= 0 and playerIdx < len(opponents):
                        askedPlayer = opponents[playerIdx]
                        validPlayer = True
                    else:
                        print("")
                        print("Invalid player - please choose again!")
                except ValueError:
                    for player in opponents:
                        if player.name.lower() == playerChoice.lower():
                            askedPlayer = player
                            validPlayer = True
                    if not validPlayer:
                        print("")
                        print("Invalid player - please choose again!")

        ranks = self.giveRanks()
        validRank = False
        while not validRank:
            print("")
            print("Which rank would you like to request?")
            for idx in range(len(ranks)):
                print(f"  {idx+1}. {ranks[idx]}")
            rankChoice = input(" --> ")

            try:
                rankIdx = int(rankChoice) - 1
                if rankIdx >= 0 and rankIdx < len(ranks):
                    requestedRank = ranks[rankIdx]
                    validRank = True
                else:
                    print("")
                    print("Invalid rank - please choose again!")
            except ValueError:
                for rank in ranks:
                    if rank.lower() == rankChoice.lower():
                        requestedRank = rank
                        validRank = True
                if not validRank:
                    print("")
                    print("Invalid rank - please choose again!")

        return askedPlayer, requestedRank

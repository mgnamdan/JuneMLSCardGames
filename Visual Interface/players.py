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
    pass




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
    pass

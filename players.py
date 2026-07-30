# This file will contain the class definitions for the human and computer players
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
        if self.score > 16:
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
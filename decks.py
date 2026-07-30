# This file will contain the class definition for the deck object
from cards import PlayingCard
from random import shuffle


class NormalDeck:

    RANKS = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
             "Ten", "Jack", "Queen", "King", "Ace"]
    SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]


    def __init__(self, numDecks=1):
        self.numDecks = numDecks
        self.reset(self.numDecks)


    def reset(self, numDecks):
        self.drawPile = []
        self.discardPile = []
        self.outPile = []

        for _ in range(numDecks):
            for suit in self.SUITS:
                for rank in self.RANKS:
                    newCard = PlayingCard(rank, suit)
                    self.drawPile.append(newCard)


    def __str__(self):
        return "\n".join([str(card) for card in self.drawPile])


    def draw(self):
        drawnCard = self.drawPile.pop(0)
        self.outPile.append(drawnCard)
        return drawnCard


    def discard(self, toDiscard):
        if toDiscard in self.outPile:
            self.outPile.remove(toDiscard)
            self.discardPile.append(toDiscard)


    def shuffle(self):
        shuffle(self.drawPile)

from card import Card
from deck import Deck

class Pile:
    def __init__(self, type) -> None:
        self.cards = []
        self.type = type

    def add(self, card:Card):
        self.cards.append(card)
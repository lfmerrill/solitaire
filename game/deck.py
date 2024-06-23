from card import Card
import random

class Deck:
    def __init__(self) -> None:
        self.cards = []

    def shuffle_cards(self):
        random.shuffle(self.cards)
        
    def add(self, card:Card):
        self.cards.append(card)

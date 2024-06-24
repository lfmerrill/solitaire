from card import Card
import random

class Deck:
    def __init__(self) -> None:
        self.cards = []

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def add(self, card:Card):
        self.cards.append(card)

    def prepare_deck(self):
        suits = ['clubs', 'diamonds', 'hearts', 'spades']
        ranks = ['ace', '2', '3', '4', '5', '6', '7', '8',
                    '9', '10', 'jack', 'queen', 'king']
        for suit in suits:
            for rank in ranks:
                self.add(Card(suit,rank))

    def deal_card(self):
        return self.cards.pop()

        

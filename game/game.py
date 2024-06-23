from card import Card
from pile import Pile
from deck import Deck


def main():
    deck = Deck()
    suits = ['clubs', 'diamonds', 'hearts', 'spades']
    ranks = ['ace', '2', '3', '4', '5', '6', '7', '8',
                    '9', '10', 'jack', 'queen', 'king']
    
    for suit in suits:
        for rank in ranks:
            deck.add(Card(suit,rank))
    
    # print(deck.cards)

    deck.shuffle_cards()
    print(deck.cards)




if __name__ == '__main__':
    main()
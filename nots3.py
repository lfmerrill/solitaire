import pygame
import random

class Deck:
    def __init__(self) -> None:
        self.cards = []

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def add(self, card):
        self.cards.append(card)

    def prepare_deck(self):
        suits = ['clubs', 'diamonds', 'hearts', 'spades']
        ranks = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
        for suit in suits:
            for rank in ranks:
                self.add(Card(suit, rank))

    def deal_card(self):
        return self.cards.pop()

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.image = pygame.image.load(f'images/{rank}_of_{suit}.png')
        self.image = self.resize_image(self.image, (80, 120))  # Resize the image to 80x120 pixels
        self.color = 'red' if suit in ['hearts', 'diamonds'] else 'black'
        self.revealed = False
        self.position = (0, 0)  # Initialize card position

    def resize_image(self, image, size):
        return pygame.transform.scale(image, size)

    def draw(self, screen, pos):
        self.position = pos  # Update card position
        screen.blit(self.image, pos)

    def is_clicked(self, mouse_pos):
        x, y = self.position
        width, height = self.image.get_size()
        return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

    def __str__(self) -> str:
        if self.suit in ['hearts', 'diamonds']:
            return f"{self.rank} of \033[31m{self.suit}\033[0m"
        return f"{self.rank} of \033[34m{self.suit}\033[0m"
    
    def __repr__(self) -> str:
        if self.suit in ['hearts', 'diamonds']:
            return f"{self.rank} of \033[31m{self.suit}\033[0m"
        return f"{self.rank} of \033[34m{self.suit}\033[0m"

class Solitaire:
    def __init__(self):
        self.deck = Deck()
        self.deck.prepare_deck()
        self.deck.shuffle_cards()
        self.tableau = [[] for _ in range(7)]
        self.foundation = [[] for _ in range(4)]
        self.stock = []
        self.waste = []

    def deal_tableau(self):
        for i in range(7):
            for j in range(i, 7):
                card = self.deck.deal_card()
                if i == j:
                    card.revealed = True
                self.tableau[j].append(card)

    def draw(self, screen):
        # Example draw method to visualize the tableau piles
        for i, pile in enumerate(self.tableau):
            for j, card in enumerate(pile):
                card.draw(screen, (i * 100, j * 30))  # Adjust positioning as needed

    def handle_click(self, mouse_pos):
        for pile in self.tableau:
            for card in pile:
                if card.is_clicked(mouse_pos):
                    # print(card)
                    return card

# Usage example
pygame.init()
screen = pygame.display.set_mode((800, 600))
solitaire = Solitaire()
solitaire.deal_tableau()
solitaire.draw(screen)
pygame.display.flip()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            clicked_card = solitaire.handle_click(mouse_pos)
            if clicked_card:
                print(f"Clicked card: {clicked_card}")

pygame.quit()

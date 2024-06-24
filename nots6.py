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
        self.selected = False

    def resize_image(self, image, size):
        return pygame.transform.scale(image, size)

    def draw(self, screen, pos):
        self.position = pos  # Update card position
        if self.selected:
            pygame.draw.rect(screen, (255, 255, 0), (self.position[0] - 2, self.position[1] - 2, 84, 124), 3)
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
        self.selected_card = None

    def deal_tableau(self):
        for i in range(7):
            for j in range(i, 7):
                card = self.deck.deal_card()
                if i == j:
                    card.revealed = True
                self.tableau[j].append(card)

    def draw(self, screen):
        # Draw tableau piles
        tableau_start_y = 150  # Adjust the starting y position for tableau piles
        for i, pile in enumerate(self.tableau):
            for j, card in enumerate(pile):
                card.draw(screen, (i * 100, tableau_start_y + j * 30))  # Adjust positioning as needed
        
        # Draw foundation piles
        foundation_x = 300  # Starting x position for foundation piles
        foundation_y = 20  # Adjust the y position for foundation piles
        for i, pile in enumerate(self.foundation):
            if pile:
                pile[-1].draw(screen, (foundation_x + i * 100, foundation_y))  # Draw the top card of each foundation pile
            else:
                # Draw an empty placeholder for foundation piles
                pygame.draw.rect(screen, (128, 128, 128), (foundation_x + i * 100, foundation_y, 80, 120), 2)

    def handle_click(self, mouse_pos):
        for pile in self.tableau:
            for card in pile:
                if card.is_clicked(mouse_pos):
                    if self.selected_card:
                        self.move_card(card, pile)
                    else:
                        self.select_card(card)
                    return card
        # Check foundation piles for clicks
        foundation_x = 300  # Starting x position for foundation piles
        foundation_y = 20  # Adjust the y position for foundation piles
        for i, pile in enumerate(self.foundation):
            if len(pile) > 0 and pile[-1].is_clicked(mouse_pos):
                if self.selected_card:
                    self.move_card_to_foundation(pile)
                else:
                    self.select_card(pile[-1])
                return pile[-1]
            elif foundation_x + i * 100 <= mouse_pos[0] <= foundation_x + i * 100 + 80 and foundation_y <= mouse_pos[1] <= foundation_y + 120:
                if self.selected_card:
                    self.move_card_to_foundation(pile)
                return

    def select_card(self, card):
        if self.selected_card:
            self.selected_card.selected = False
        self.selected_card = card
        self.selected_card.selected = True

    def move_card(self, card, new_pile):
        # Just a simple move, you can add logic to check rules later
        if self.selected_card:
            for pile in self.tableau:
                if self.selected_card in pile:
                    pile.remove(self.selected_card)
                    new_pile.append(self.selected_card)
                    self.selected_card.selected = False
                    self.selected_card = None
                    return

    def move_card_to_foundation(self, foundation_pile):
        if self.selected_card:
            for pile in self.tableau:
                if self.selected_card in pile:
                    pile.remove(self.selected_card)
                    foundation_pile.append(self.selected_card)
                    self.selected_card.selected = False
                    self.selected_card = None
                    return

# Usage example
pygame.init()
screen = pygame.display.set_mode((1200, 800))  # Increase screen size
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
    screen.fill((0, 128, 0))  # Clear screen with green background
    solitaire.draw(screen)
    pygame.display.flip()

pygame.quit()

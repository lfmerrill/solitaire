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
        self.stock = self.deck.cards.copy()
        self.waste = []
        self.selected_card = None
        self.selected_stack = []
        self.deal_tableau()

    def deal_tableau(self):
        for i in range(7):
            for j in range(i, 7):
                card = self.stock.pop()
                if i == j:
                    card.revealed = True
                self.tableau[j].append(card)

    def draw(self, screen):
        # Draw tableau piles
        tableau_start_y = 150  # Adjust the starting y position for tableau piles
        for i, pile in enumerate(self.tableau):
            if pile:
                for j, card in enumerate(pile):
                    card.draw(screen, (i * 100, tableau_start_y + j * 30))  # Adjust positioning as needed
            else:
                # Draw placeholder for empty tableau pile
                pygame.draw.rect(screen, (128, 128, 128), (i * 100, tableau_start_y, 80, 120))

        # Draw foundation piles
        foundation_x = 400  # Starting x position for foundation piles
        foundation_y = 20  # Adjust the y position for foundation piles
        for i, pile in enumerate(self.foundation):
            if pile:
                pile[-1].draw(screen, (foundation_x + i * 100, foundation_y))  # Draw the top card of each foundation pile
            else:
                # Draw an empty placeholder for foundation piles
                pygame.draw.rect(screen, (0, 128, 0), (foundation_x + i * 100, foundation_y, 80, 120), 2)

        # Draw stock pile
        if self.stock:
            pygame.draw.rect(screen, (0, 0, 0), (20, 20, 80, 120))
        else:
            pygame.draw.rect(screen, (128, 128, 128), (20, 20, 80, 120))

        # Draw waste pile
        if self.waste:
            self.waste[-1].draw(screen, (120, 20))

    def handle_click(self, mouse_pos):
        # Check tableau piles for clicks
        for i, pile in enumerate(self.tableau):
            if not pile:
                # Check click on empty tableau placeholder
                if i * 100 <= mouse_pos[0] <= i * 100 + 80 and 150 <= mouse_pos[1] <= 150 + 120:
                    print(f"Clicked on empty tableau pile {i + 1}")
                    if self.selected_card and self.selected_card.rank == 'king':
                        self.move_stack(pile)
                    return
            else:
                for card in reversed(pile):  # Iterate in reverse order to check top cards first
                    if card.is_clicked(mouse_pos):
                        print(f"Clicked on tableau pile {i + 1}")
                        if self.selected_card:
                            if self.selected_card == card:
                                self.deselect_card()
                            else:
                                self.move_stack(pile)
                        else:
                            self.select_card(card, pile)
                        return card

        # Check foundation piles for clicks
        foundation_x = 400  # Starting x position for foundation piles
        foundation_y = 20  # Adjust the y position for foundation piles
        for i, pile in enumerate(self.foundation):
            if len(pile) > 0 and pile[-1].is_clicked(mouse_pos):
                print(f"Clicked on foundation pile {i + 1}")
                if self.selected_card:
                    if self.selected_card == pile[-1]:
                        self.deselect_card()
                    else:
                        self.move_stack(pile)
                else:
                    self.select_card(pile[-1], pile)
                return pile[-1]
            elif foundation_x + i * 100 <= mouse_pos[0] <= foundation_x + i * 100 + 80 and foundation_y <= mouse_pos[1] <= foundation_y + 120:
                print(f"Clicked on empty foundation pile {i + 1}")
                if self.selected_card and self.selected_card.rank == 'ace':
                    self.move_stack(pile)
                return

        # Check stock pile for clicks
        if 20 <= mouse_pos[0] <= 100 and 20 <= mouse_pos[1] <= 140:
            self.deal_stock_card()
            return

        # Check waste pile for clicks
        if self.waste and self.waste[-1].is_clicked(mouse_pos):
            print("Clicked on waste pile")
            if self.selected_card:
                if self.selected_card == self.waste[-1]:
                    self.deselect_card()
                else:
                    self.move_stack(self.waste)
            else:
                self.select_card(self.waste[-1], self.waste)
            return self.waste[-1]

    def deal_stock_card(self):
        if self.stock:
            card = self.stock.pop()
            card.revealed = True
            self.waste.append(card)
        elif self.waste:
            self.stock = self.waste[::-1]
            for card in self.stock:
                card.revealed = False
            self.waste = []

    def select_card(self, card, pile):
        if self.selected_card == card:
            self.deselect_card()
        else:
            if self.selected_card:
                self.selected_card.selected = False
            self.selected_card = card
            self.selected_card.selected = True
            self.selected_stack = pile[pile.index(card):]  # Select the card and all cards below it

    def deselect_card(self):
        if self.selected_card:
            self.selected_card.selected = False
            self.selected_card = None
            self.selected_stack = []

    def move_stack(self, new_pile):
        if self.selected_stack and self.is_valid_move(self.selected_stack[0], new_pile):
            for card in self.selected_stack:
                self.remove_card(card)
                new_pile.append(card)
            self.selected_card.selected = False
            self.selected_card = None
            self.selected_stack = []

    def remove_card(self, card):
        for pile in self.tableau:
            if card in pile:
                pile.remove(card)
                return
        if card in self.waste:
            self.waste.remove(card)
            return
        for pile in self.foundation:
            if card in pile:
                pile.remove(card)
                return

    def is_valid_move(self, card, new_pile):
        if not new_pile:
            # Only Kings can be moved to empty tableau piles
            if new_pile in self.tableau and card.rank == 'king':
                return True
            # Only Aces can be moved to empty foundation piles
            if new_pile in self.foundation and card.rank == 'ace':
                return True
        elif new_pile in self.foundation:
            top_card = new_pile[-1]
            return card.suit == top_card.suit and self.rank_value(card.rank) == self.rank_value(top_card.rank) + 1
        elif new_pile in self.tableau:
            top_card = new_pile[-1]
            return card.color != top_card.color and self.rank_value(card.rank) == self.rank_value(top_card.rank) - 1
        return False

    def rank_value(self, rank):
        values = {
            'ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, '10': 10, 'jack': 11, 'queen': 12, 'king': 13
        }
        return values[rank]

# Usage example
pygame.init()
screen = pygame.display.set_mode((1200, 800))  # Increase screen size
solitaire = Solitaire()
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

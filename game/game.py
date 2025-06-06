from .card import Card
from .deck import Deck
import pygame


class Solitaire:
    def __init__(self):
        self.deck = Deck()
        self.new_game()

    def new_game(self):
        self.deck.cards = []
        self.deck.prepare_deck()
        self.deck.shuffle_cards()
        self.tableau = [[] for _ in range(7)]
        self.foundation = [[] for _ in range(4)]
        self.stock = self.deck.cards.copy()
        self.waste = []
        self.selected_card = None
        self.selected_stack = []
        self.won = False

        # Reset all cards
        for card in self.stock:
            card.revealed = False
            card.selected = False

        self.deal_tableau()

    def deal_tableau(self):
        for i in range(7):
            for j in range(i, 7):
                card = self.stock.pop()
                if j == i:
                    card.revealed = True
                self.tableau[j].append(card)

    def draw(self, screen):
        tableau_start_y = 150  
        for i, pile in enumerate(self.tableau):
            if pile:
                for j, card in enumerate(pile):
                    card.draw(screen, (i * 100, tableau_start_y + j * 30))  
            else:
                pygame.draw.rect(screen, (128, 128, 128), (i * 100, tableau_start_y, 80, 120))

        foundation_x = 400  
        foundation_y = 20  
        for i, pile in enumerate(self.foundation):
            if pile:
                pile[-1].draw(screen, (foundation_x + i * 100, foundation_y))  
            else:
                pygame.draw.rect(screen, (128, 128, 128), (foundation_x + i * 100, foundation_y, 80, 120), 2)

        if self.stock:
            pygame.draw.rect(screen, (0, 0, 0), (20, 20, 80, 120))
        else:
            pygame.draw.rect(screen, (128, 128, 128), (20, 20, 80, 120))

        if self.waste:
            self.waste[-1].draw(screen, (120, 20))

        pygame.draw.rect(screen, (0, 0, 255), (1050, 20, 160, 40))
        font = pygame.font.Font(None, 36)
        text = font.render("New Game", True, (255, 255, 255))
        screen.blit(text, (1060, 25))

        if self.won:
            font = pygame.font.Font(None, 74)
            text = font.render("You Won!", True, (255, 215, 0))
            screen.blit(text, (500, 400))

    def handle_click(self, mouse_pos):
        # Check if "New Game" button is clicked
        if 1050 <= mouse_pos[0] <= 1170 and 20 <= mouse_pos[1] <= 60:
            self.new_game()
            return

        # Check tableau piles for clicks
        for i, pile in enumerate(self.tableau):
            if not pile:
                # Check click on empty tableau placeholder
                if i * 100 <= mouse_pos[0] <= i * 100 + 80 and 150 <= mouse_pos[1] <= 150 + 120:
                    # print(f"Clicked on empty tableau pile {i + 1}")
                    if self.selected_card and self.selected_card.rank == 'king':
                        self.move_stack(pile)
                    return
            else:
                for card in reversed(pile): 
                    if card.is_clicked(mouse_pos):
                        # print(f"Clicked on tableau pile {i + 1}")
                        if self.selected_card:
                            if self.selected_card == card:
                                self.deselect_card()
                            else:
                                self.move_stack(pile)
                        else:
                            self.select_card(card, pile)
                        return card

        # Check foundation piles for clicks
        foundation_x = 400  
        foundation_y = 20  
        for i, pile in enumerate(self.foundation):
            if len(pile) > 0 and pile[-1].is_clicked(mouse_pos):
                # print(f"Clicked on foundation pile {i + 1}")
                if self.selected_card:
                    if self.selected_card == pile[-1]:
                        self.deselect_card()
                    else:
                        self.move_card_to_foundation(pile)
                else:
                    self.select_card(pile[-1], pile)
                return pile[-1]
            elif foundation_x + i * 100 <= mouse_pos[0] <= foundation_x + i * 100 + 80 and foundation_y <= mouse_pos[1] <= foundation_y + 120:
                # print(f"Clicked on empty foundation pile {i + 1}")
                if self.selected_card and self.selected_card.rank == 'ace':
                    self.move_card_to_foundation(pile)
                return

        # Check stock pile for clicks
        if 20 <= mouse_pos[0] <= 100 and 20 <= mouse_pos[1] <= 140:
            self.deal_stock_card()
            return

        # Check waste pile for clicks
        if self.waste and self.waste[-1].is_clicked(mouse_pos):
            # print("Clicked on waste pile")
            if self.selected_card:
                if self.selected_card == self.waste[-1]:
                    self.deselect_card()
                else:
                    self.move_stack(self.waste)
            else:
                self.select_card(self.waste[-1], self.waste)
            return self.waste[-1]

    def deal_stock_card(self):
        self.deselect_all_cards()  
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
            self.selected_stack = pile[pile.index(card):]  

    def deselect_card(self):
        if self.selected_card:
            self.selected_card.selected = False
            self.selected_card = None
            self.selected_stack = []

    def deselect_all_cards(self):
        if self.selected_card:
            self.selected_card.selected = False
            self.selected_card = None
        self.selected_stack = []

    def move_stack(self, new_pile):
        if self.selected_stack and self.is_valid_move(self.selected_stack[0], new_pile, is_stack=True):
            for card in self.selected_stack:
                self.remove_card(card)
                new_pile.append(card)
            self.selected_card.selected = False
            self.selected_card = None
            self.selected_stack = []
            self.check_win()

    def move_card_to_foundation(self, foundation_pile):
        if self.selected_card and self.is_valid_move(self.selected_card, foundation_pile, is_stack=False):
            self.remove_card(self.selected_card)
            foundation_pile.append(self.selected_card)
            self.selected_card.selected = False
            self.selected_card = None
            self.selected_stack = []
            self.check_win()

    def remove_card(self, card):
        for pile in self.tableau:
            if card in pile:
                pile.remove(card)
                if pile and not pile[-1].revealed:
                    pile[-1].revealed = True
                return
        if card in self.waste:
            self.waste.remove(card)
            return
        for pile in self.foundation:
            if card in pile:
                pile.remove(card)
                return

    def is_valid_move(self, card, new_pile, is_stack):
        if not new_pile:
            if new_pile in self.tableau and card.rank == 'king':
                return True
            if new_pile in self.foundation and card.rank == 'ace':
                return True
        elif new_pile in self.foundation:
            if is_stack:
                return False  
            top_card = new_pile[-1]
            return card.suit == top_card.suit and self.rank_value(card.rank) == self.rank_value(top_card.rank) + 1
        elif new_pile in self.tableau:
            top_card = new_pile[-1] if new_pile else None
            return (top_card is None and card.rank == 'king') or (top_card and card.color != top_card.color and self.rank_value(card.rank) == self.rank_value(top_card.rank) - 1)
        return False

    def rank_value(self, rank):
        values = {
            'ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, '10': 10, 'jack': 11, 'queen': 12, 'king': 13
        }
        return values[rank]

    def check_win(self):
        if all(len(pile) == 13 for pile in self.foundation):
            self.won = True

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))  
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
                # if clicked_card:
                #     # print(f"Clicked card: {clicked_card}")
        screen.fill((0, 128, 0))  
        solitaire.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ =="__main__":
    main()
import pygame

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.front_image = pygame.image.load(f'images/{rank}_of_{suit}.png')
        self.back_image = pygame.image.load('images/back_of_card.png')
        self.front_image = self.resize_image(self.front_image, (80, 120))  # Resize the image to 80x120 pixels
        self.back_image = self.resize_image(self.back_image, (80, 120))    # Resize the back image to 80x120 pixels
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
        if self.revealed:
            screen.blit(self.front_image, pos)
        else:
            screen.blit(self.back_image, pos)

    def is_clicked(self, mouse_pos):
        if not self.revealed:
            return False
        x, y = self.position
        width, height = self.front_image.get_size()
        return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

    def __str__(self) -> str:
        if self.suit in ['hearts', 'diamonds']:
            return f"{self.rank} of \033[31m{self.suit}\033[0m"
        return f"{self.rank} of \033[34m{self.suit}\033[0m"
    
    def __repr__(self) -> str:
        if self.suit in ['hearts', 'diamonds']:
            return f"{self.rank} of \033[31m{self.suit}\033[0m"
        return f"{self.rank} of \033[34m{self.suit}\033[0m"
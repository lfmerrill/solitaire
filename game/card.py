import pygame

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.image = pygame.image.load(f'images/{rank}_of_{suit}.png')
        self.color = 'red'
        self.revealed = False

    def __str__(self) -> str:
        if self.suit == 'hearts' or self.suit == 'diamonds':
            return f"{self.rank} of \033[31m{self.suit}\033[0m"
        return f"{self.rank} of \033[34m{self.suit}\033[0m"
    
    def __repr__(self) -> str:
        # print("\033[31mThis is red text\033[0m")
        # print("\033[34mThis is blue text\033[0m")
        if self.suit == 'hearts' or self.suit == 'diamonds':
            return f"{self.rank} of \033[31m{self.suit}\033[0m"
        return f"{self.rank} of \033[34m{self.suit}\033[0m"
    
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
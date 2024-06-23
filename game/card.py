import pygame

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.image = pygame.image.load(f'images/{rank}_of_{suit}.png')
        self.color = 'red'
        self.revealed = False

    def draw(self, screen, pos):
        screen.blit(self.image, pos)
# import pygame

# display_dimensions = (1100, 800)

# pygame.init()

# game_display = pygame.display.set_mode(display_dimensions)

# pygame.display.set_caption('Solitare')

# clock = pygame.time.Clock()
# FPS = 10


# def quit_game():
#     pygame.quit()
#     quit()


import sys, pygame
pygame.init()

size = width, height = 1440, 1440
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("images/2_of_clubs.png")
ballrect = ball.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
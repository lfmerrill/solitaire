import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Draw Shapes with Pygame')

# Set colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    window.fill(white)

    # Draw a rectangle
    pygame.draw.rect(window, red, (100, 100, 200, 150))

    # Draw a circle
    pygame.draw.circle(window, green, (400, 300), 50)

    # Draw a line
    pygame.draw.line(window, blue, (550, 500), (700, 500), 10)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

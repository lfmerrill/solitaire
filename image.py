# your_game_module.py

import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    width, height = 800, 600
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Card Game')

    # Set colors
    white = (255, 255, 255)
    table_green = (42,128,43)

    # Load an image
    card_image = pygame.image.load('images/2_of_clubs.png')
    card_image = pygame.transform.scale(card_image, (66, 100))

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        window.fill(table_green)

        # Blit the card image
        window.blit(card_image, (350, 225))

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

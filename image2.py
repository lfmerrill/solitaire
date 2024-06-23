import pygame
import sys

def draw_rounded_rect(surface, color, rect, corner_radius):
    """ Draw a rectangle with rounded corners. """
    x, y, width, height = rect
    if corner_radius > min(width, height) // 2:
        corner_radius = min(width, height) // 2

    pygame.draw.rect(surface, color, (x + corner_radius, y, width - 2 * corner_radius, height))
    pygame.draw.rect(surface, color, (x, y + corner_radius, width, height - 2 * corner_radius))

    pygame.draw.circle(surface, color, (x + corner_radius, y + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (x + width - corner_radius, y + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (x + corner_radius, y + height - corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (x + width - corner_radius, y + height - corner_radius), corner_radius)

def draw_rounded_rect_with_outline(surface, rect, corner_radius, fill_color, outline_color, outline_width):
    """ Draw a rounded rectangle with an outline. """
    outline_rect = (rect[0] - outline_width, rect[1] - outline_width, rect[2] + 2 * outline_width, rect[3] + 2 * outline_width)
    draw_rounded_rect(surface, outline_color, outline_rect, corner_radius + outline_width)
    draw_rounded_rect(surface, fill_color, rect, corner_radius)

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    width, height = 800, 600
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Card Game')

    # Set colors
    white = (255, 255, 255)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    table_green = (42,128,43)

    # Load an image (make sure you have an image file in the same directory or provide the correct path)
    card_image = pygame.image.load('images/2_of_clubs.png')
    card_image = pygame.transform.scale(card_image, (100, 150))

    # Position of the card
    card_rect = card_image.get_rect(topleft=(600, 225))

    # Main loop
    running = True
    selected = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if card_rect.collidepoint(event.pos):
                    selected = not selected


        # Fill the background with white
        window.fill(table_green)

        

        # Draw the outline if selected
        if selected:
            draw_rounded_rect_with_outline(window, card_rect.inflate(10, 10), 10, white, green, 5)

        # Draw the card image
        window.blit(card_image, card_rect.topleft)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

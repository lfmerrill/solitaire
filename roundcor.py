import pygame
import sys

def draw_rounded_rect(surface, color, rect, corner_radius):
    """ Draw a rectangle with rounded corners. 
    Argument:
    surface: pygame surface where the rectangle will be drawn.
    color: the color of the rectangle.
    rect: a tuple containing the rectangle's x, y, width, and height.
    corner_radius: the radius of the rounded corners.
    """
    x, y, width, height = rect
    # Ensure the corner radius isn't too large
    if corner_radius > min(width, height) // 2:
        corner_radius = min(width, height) // 2

    # Draw the central rectangle
    pygame.draw.rect(surface, color, (x + corner_radius, y, width - 2 * corner_radius, height))
    pygame.draw.rect(surface, color, (x, y + corner_radius, width, height - 2 * corner_radius))

    # Draw the four corner circles
    pygame.draw.circle(surface, color, (x + corner_radius, y + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (x + width - corner_radius, y + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (x + corner_radius, y + height - corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (x + width - corner_radius, y + height - corner_radius), corner_radius)

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Rounded Rectangle with Pygame')

# Set colors
white = (255, 255, 255)
blue = (0, 0, 255)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    window.fill(white)

    # Draw a rounded rectangle
    draw_rounded_rect(window, (25,128,43), (200, 150, 350, 450), 50)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

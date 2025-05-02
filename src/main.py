import pygame
import sys
import config
import map
from arena import Arena

# Initialization
pygame.init()

# Create window
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Roboarena")
clock = pygame.time.Clock()

# Game setup
arena = Arena(screen, config.ROWS, config.COLUMNS, map.COLORS)
arena.create_map(map.get_map1())

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill((220, 220, 220))  # light gray background
    arena.draw_map()
    pygame.display.flip()
    clock.tick(60)

# Cleanup
pygame.quit()
sys.exit()

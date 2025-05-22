import pygame
import sys
import config
import map
from arena import Arena
from robot import Robot

# Initialisation
pygame.init()

# Get current screen resolution
info = pygame.display.Info()
max_width, max_height = info.current_w, info.current_h

# Calculate TILE_SIZE to fit the fixed grid into the screen
config.TILE_SIZE = min(max_width // config.COLUMNS, max_height // config.ROWS)

# set window size
window_width = config.TILE_SIZE * config.COLUMNS
window_height = config.TILE_SIZE * config.ROWS

# Create window (not fullscreen)
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Roboarena")
clock = pygame.time.Clock()

# Debug info
print(f"Monitor: {max_width}x{max_height}")
print(f"Fenster: {window_width}x{window_height}")
print(f"TILE_SIZE: {config.TILE_SIZE}")

# Load map and arena
arena = Arena(screen, config.ROWS, config.COLUMNS, config.COLORS)
arena.create_map(map.get_map("test-level.txt"))

# Create robots
robot1 = Robot(screen, 500, 500, 20, 180, (255, 255, 255))
robot2 = Robot(screen, 800, 300, 30, 0, (0, 100, 190))
robot3 = Robot(screen, 300, 600, 40, 50, (255, 50, 120))

player = robot1


# Movement
vel = 2
turn_speed = 5


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False

    keys = pygame.key.get_pressed()

    player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * vel
    player.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * vel
    player.alpha += (keys[pygame.K_d] - keys[pygame.K_a]) * turn_speed

    screen.fill((220, 220, 220))  # light gray background
    arena.draw_map()
    robot1.draw_robot()
    robot2.draw_robot()
    robot3.draw_robot()
    pygame.display.flip()

pygame.quit()
sys.exit()

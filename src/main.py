import pygame
import sys
import config
import map
from arena import Arena
from robot import Robot

# Initialization
pygame.init()

# Create window
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Roboarena")
clock = pygame.time.Clock()

# Game setup
arena = Arena(screen, config.ROWS, config.COLUMNS, map.COLORS)
arena.create_map(map.get_map1())

player = Robot(screen, 500, 500, 20, 180, (255, 255, 255), 1, 1)
enemy1 = Robot(screen, 800, 300, 30, 0, (0, 100, 190), 1, 1)
enemy2 = Robot(screen, 300, 600, 40, 50, (255, 50, 120), 1, 1)
enemy3 = Robot(screen, 1200, 600, 40, 50, (0, 250, 0), 1, 1)

robots = [player, enemy1, enemy2, enemy3]

circle_tick = 50
angle = 180


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
    ticks = pygame.time.get_ticks()
    player.update_player(robots)
    if ticks > circle_tick:
        circle_tick += 50
        angle = (angle + 3) % 360
    enemy1.move_circle([800, 300], 50, angle, robots)
    enemy2.update_enemy(player, robots)
    enemy3.update_enemy(player, robots)
    pygame.display.flip()
    clock.tick(60)

# Cleanup
pygame.quit()
sys.exit()

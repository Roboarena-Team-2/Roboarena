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
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            print(pygame.key.name(event.key))
            if event.key == pygame.K_ESCAPE:
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

# Cleanup
pygame.quit()
sys.exit()

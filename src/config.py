import pygame


# Global constants

# Tile textures by type
TEXTURES = {
    "boden": pygame.image.load("../resources/Textures/Floor.png"),  # ground
    "rand": pygame.image.load("../resources/Textures/Wall.png"),  # walls
    "lava": pygame.image.load("../resources/Textures/Lava.png"),  # lava
    "eis": pygame.image.load("../resources/Textures/Ice.png"),  # ice
    "sand": pygame.image.load("../resources/Textures/Sand.png"),  # sand
    "gebuesch": pygame.image.load("../resources/Textures/Bush.png"),  # bush
}

TILE_SIZE = 0  # will be assigned during runtime in main.py
COLUMNS = 48  # number of tile columns (horizontal)
ROWS = 27  # number of tile rows (vertical)

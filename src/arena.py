import pygame
import config


class Arena:
    def __init__(self, screen, rows, columns, textures):
        self.screen = screen  # current game screen
        self.rows = rows  # number of rows
        self.columns = columns  # number of columns
        self.textures = textures  # possible tile textures
        self.grid = None  # will hold the tile data (for drawing)
        self.initialise_map()  # fill grid with floor and outer walls

    def initialise_map(self):
        self.grid = []
        for r in range(self.rows):
            current_row = []
            for c in range(self.columns):
                if c == 0 or r == 0 or r == self.rows - 1 or c == self.columns - 1:
                    current_row.append("wall")  # outer edges
                else:
                    current_row.append("ground")  # inner tiles
            self.grid.append(current_row)

    def create_map(self, map_data):
        expected_rows = self.rows - 2
        expected_columns = self.columns - 2
        for row in map_data:  # check if map_data is in invalid format
            if len(map_data) != expected_rows:
                raise ValueError(
                    f"Map must have exactly {expected_rows}"
                    f" rows but got {len(map_data)}."
                )
            if len(row) != expected_columns:
                raise ValueError(
                    f"Map must have exactly {expected_columns}"
                    f" rows but got {len(row)}."
                )
        for r in range(expected_rows):
            for c in range(expected_columns):
                self.grid[r + 1][c + 1] = map_data[r][
                    c
                ]  # assign inner tiles of current
                # map to map_data with format-Offset 1

    def draw_map(self):
        for row in range(self.rows):
            for col in range(self.columns):
                x = col * config.TILE_SIZE
                y = row * config.TILE_SIZE
                tile_type = self.grid[row][col]
                texture = self.textures[tile_type]
                # draw the tile
                texture = texture.convert()
                texture = pygame.transform.scale(texture, (config.TILE_SIZE, config.TILE_SIZE)) 
                self.screen.blit(texture, (x, y))

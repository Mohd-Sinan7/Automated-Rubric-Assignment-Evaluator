import pygame
import random

class Food:
    def __init__(self, grid_width, grid_height, cell_size, occupied_cells=()):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        self.x = 0
        self.y = 0
        self.respawn(occupied_cells)

    def respawn(self, occupied_cells):
        # Pick from the free cells directly: never lands on the snake, and
        # can't loop forever when the board is (almost) full.
        occupied = set(occupied_cells)
        free_cells = [
            (x, y)
            for x in range(self.grid_width)
            for y in range(self.grid_height)
            if (x, y) not in occupied
        ]
        if not free_cells:
            return False
        self.x, self.y = random.choice(free_cells)
        return True

    def rect(self):
        return pygame.Rect(self.x * self.cell_size, self.y * self.cell_size, self.cell_size, self.cell_size)

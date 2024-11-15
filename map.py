import random

import pygame

from config import WIDTH, HEIGHT


class Tile:
    def __init__(self, name, image, solid, health=0):
        self.name = name
        self.image = image
        self.solid = solid
        self.health = health
        self.rect = None  # Initialize rect as None

    def reduce_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True
        return False

    def change_type(self, new_type, new_image, solid):
        self.name = new_type
        self.image = new_image
        self.solid = solid
        print(f"Tile changed to: {self.name}, Solid: {self.solid}")

    @property
    def left(self):
        return self.rect.left

    @property
    def right(self):
        return self.rect.right

    @property
    def top(self):
        return self.rect.top

    @property
    def bottom(self):
        return self.rect.bottom


class Map:
    def __init__(self, map_file, tile_kind):
        self.map_file = map_file
        self.tile_kind = tile_kind
        self.tile_size = tile_size
        self.tiles = []
        self.solid_tiles = []
        self.tile_images = []

        # Set up tiles from the loaded maps
        for line in self.map_file:
            row = []
            for tile_number in line:
                row.append(int(tile_number))
            self.tiles.append(row)

    def load(self):
        # Go row by row
        for y, row in enumerate(self.tiles):
            # Within the current row, go through each tile
            for x, tile in enumerate(row):
                location = (x * self.tile_size, y * self.tile_size)
                image = pygame.image.load(self.tile_kind[tile].image).convert_alpha()
                self.tile_images.append((image, location))

                # If the tile is solid, create a Tile object and store it for collision detection
                if tile == 1 or tile == 2:
                    solid_tile = Tile(self.tile_kind[tile].name, image, True, health=10)
                    solid_tile.rect = pygame.Rect(location[0], location[1], self.tile_size, self.tile_size)
                    self.solid_tiles.append(solid_tile)

    def draw(self, screen):
        # Use blits to draw all updated tiles
        screen.blits(self.tile_images)

    def get_solid_tiles_with_health(self):
        return [tile for tile in self.solid_tiles if tile.health > 0]

    def replace_tile(self, tile):
        if tile.health <= 0:
            # Replace the tile with grass
            tile.change_type("grass", pygame.image.load("images/grass64.png"), False)
            # Remove from solid tiles list
            self.solid_tiles = [t for t in self.solid_tiles if t.name != "grass"]
            # Update the tile_images list
            for i, (image, location) in enumerate(self.tile_images):
                if location == (tile.rect.x, tile.rect.y):
                    self.tile_images[i] = (tile.image, location)
                    break


tile_size = 64
tile_cols = WIDTH // tile_size
tile_rows = HEIGHT // tile_size
grid = [["0" for _ in range(tile_cols + 1)] for _ in range(tile_rows + 1)]


def place_trees():
    for _ in range(random.randint(12, 24)):
        random_col = random.randint(0, tile_cols - 1)
        random_row = random.randint(0, tile_rows - 1)
        grid[random_row][random_col] = str(random.choice([1, 2]))


# Tile map
tiles_grass = [
    Tile("grass", "images/grass64.png", "False"),
    Tile("tree", "images/tree64.png", "True"),
    Tile("jungle_tree", "images/jungle_tree64.png", "True"),
]
tiles_snow = [
    Tile("snow", "images/snow64.png", "False"),
    Tile("tree", "images/snowman-snow_tile64.png", "True"),
    Tile("jungle_tree", "images/snowman-snow_tile64.png", "True"),
]

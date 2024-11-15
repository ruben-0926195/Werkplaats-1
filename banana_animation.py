import random

import pygame

import config

# Load the banana image to use on the main menu
banana_image = pygame.image.load("images/banana.png")
banana_width = banana_image.get_width()
banana_height = banana_image.get_height()
# Create a list to track the bananas on the menu background
bananas = [{"x": random.randint(0, config.WIDTH - banana_width), "y": random.randint(-config.HEIGHT, 0)} for _ in
           range(20)]


def update_bananas():
    for banana in bananas:
        banana["y"] += 3
        if banana["y"] > config.HEIGHT:
            banana["y"] = random.randint(-config.HEIGHT, 0)
            banana["x"] = random.randint(0, config.HEIGHT - banana_width)


def draw_bananas():
    for banana in bananas:
        config.screen.blit(banana_image, (banana["x"], banana["y"]))

import math

import pygame


def resize_image(image, width, height):
    return pygame.transform.scale(image, (width, height))


class Enemy:
    def __init__(self, x, y, width, height, speed, screen_width, screen_height, images):
        self.x = x
        self.y = y
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.alive = True
        self.health = 2

        self.images = [resize_image(image, width, height) for image in images]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.animation_time = 100  # milliseconds
        self.last_update_time = pygame.time.get_ticks()

    def animation(self):
        # Get the current time
        current_time = pygame.time.get_ticks()

        # Check if enough time has passed to update the animation frame
        if current_time - self.last_update_time > self.animation_time:
            self.index = (self.index + 1) % len(self.images)  # Cycle through frames
            self.image = self.images[self.index]
            self.last_update_time = current_time

    def draw(self, surface):
        if self.alive:
            # Draws the enemy on the screen
            surface.blit(self.image, self.rect.topleft)

    # ---------------------------------------------------------------
    # Parts of the code implementing enemy movement was generated with the assistance of an AI
    # Prompt used: "Create a player class and an enemy class. The player can move around using keys. The enemy should follow the player."
    # AI model: OpenAI GPT-4, Date: October 2024
    # Code has been modified for specific use case
    # ---------------------------------------------------------------
    def follow(self, player):
        if self.alive:
            # Calculate direction to move towards the player
            dx = player.x - self.rect.x
            dy = player.y - self.rect.y
            dist = math.hypot(dx, dy)  # Distance between player and enemy

            if dist != 0:  # Avoid division by zero
                dx, dy = dx / dist, dy / dist

            # Move the enemy towards the player
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
            self.animation()


class Toucan(Enemy):
    def __init__(self, x, y, screen_width, screen_height):
        width = 50
        height = 50
        speed = 1
        images = [
            pygame.image.load("images/toucan64.png").convert_alpha(),
            pygame.image.load("images/toucan64_2.png").convert_alpha(),
        ]
        super().__init__(x, y, width, height, speed, screen_width, screen_height, images)
        self.health = 1


class Alligator(Enemy):
    def __init__(self, x, y, screen_width, screen_height):
        width = 55
        height = 55
        speed = 1.5
        images = [
            pygame.image.load("images/alligator64.png").convert_alpha(),
            pygame.image.load("images/alligator64_2.png").convert_alpha(),
        ]
        super().__init__(x, y, width, height, speed, screen_width, screen_height, images)
        self.health = 2


class Penguin(Enemy):
    def __init__(self, x, y, screen_width, screen_height):
        width = 50
        height = 50
        speed = 1
        images = [
            pygame.image.load("images/Penguin64.png").convert_alpha(),
            pygame.image.load("images/Penguin64_2.png").convert_alpha(),
            pygame.image.load("images/Penguin64_3.png").convert_alpha(),
            pygame.image.load("images/Penguin64_4.png").convert_alpha(),
        ]
        super().__init__(x, y, width, height, speed, screen_width, screen_height, images)
        self.health = 1


class Snowman(Enemy):
    def __init__(self, x, y, screen_width, screen_height):
        width = 55
        height = 55
        speed = 1.5
        images = [
            pygame.image.load("images/snowman64.png").convert_alpha(),
            pygame.image.load("images/snowman64_2.png").convert_alpha(),
        ]
        super().__init__(x, y, width, height, speed, screen_width, screen_height, images)
        self.health = 1

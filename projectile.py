import pygame


# ---------------------------------------------------------------
# Parts of the code implementing projectiles was generated with the assistance of an AI
# Prompt used: "Implementing Bullets in Pygame using a class for bullet and no class for player"
# AI model: OpenAI GPT-4, Date: September 2024
# Code has been modified for specific use case
# ---------------------------------------------------------------
class Projectile:

    def __init__(self, x, y, type_):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 5
        self.rotation = 0
        self.direction = True
        self.speed = 5

        if type_ == "banana":
            self.image = pygame.image.load("images/banana.png")
            self.width = 50
            self.height = 50
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        if type_ == "coconut":
            self.image = pygame.image.load("images/coconut.png")
        if type_ == "orange":
            self.image = pygame.image.load("images/orange.png")
            self.width = 40
            self.height = 40
            self.speed = 2.5
            self.damage = 1
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        if type_ == "snowball":
            self.image = pygame.image.load("images/snowball.png")
            self.speed = 2
            self.damage = 1

        self.rect = self.image.get_rect()

    def update(self):
        # Update position of projectile
        self.y -= self.speed
        self.rect.y = self.y
        self.rect.x = self.x

    def draw(self, screen):
        # Rotate the image
        self.rotation += self.speed
        rotated_image = pygame.transform.rotate(self.image, self.rotation)

        # Get the rect of the rotated image and set its center to the original position
        rotated_image_rect = rotated_image.get_rect(center=(self.x, self.y))

        # Adjust for the offset caused by rotation
        # Calculate the offset needed to center the image correctly
        offset_x = (rotated_image_rect.width - self.image.get_width()) // 2
        offset_y = (rotated_image_rect.height - self.image.get_height()) // 2

        # Draw the rotated image on the screen with the adjusted position
        screen.blit(rotated_image, (self.x - offset_x, self.y - offset_y))

    def is_off_screen(self):
        # Check if the projectile is out of bounds
        return self.y < 0

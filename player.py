import pygame


class Player:
    def __init__(self, screen_width, screen_height, keybindings):
        self.images = [
            pygame.image.load("images/kong64_1.png").convert_alpha(),
            pygame.image.load("images/kong64_2.png").convert_alpha(),
            pygame.image.load("images/kong64_3.png").convert_alpha(),
            pygame.image.load("images/kong64_4.png").convert_alpha(),
        ]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.rect.x = (self.screen_width - self.width) // 2
        self.rect.y = (self.height - self.height) - 20

        self.keybindings = keybindings

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

    def move(self, solid_tiles):
        keys = pygame.key.get_pressed()
        direction_x, direction_y = 0, 0
        movement_speed = 8  # Adjust this as needed

        if keys[self.keybindings['move_up']]:
            direction_y -= movement_speed
            self.animation()
        if keys[self.keybindings['move_down']]:
            direction_y += movement_speed
            self.animation()
        if keys[self.keybindings['move_left']]:
            direction_x -= movement_speed
            self.animation()
        if keys[self.keybindings['move_right']]:
            direction_x += movement_speed
            self.animation()

        # Save the original position
        original_position = self.rect.copy()

        # Move horizontally first
        self.rect.x += direction_x
        for solid_tile in solid_tiles:
            if self.rect.colliderect(solid_tile):
                # Handle collision
                if direction_x > 0:  # Moving right
                    self.rect.right = solid_tile.left
                if direction_x < 0:  # Moving left
                    self.rect.left = solid_tile.right

        # Move vertically
        self.rect.y += direction_y
        for solid_tile in solid_tiles:
            if self.rect.colliderect(solid_tile):
                # Handle collision
                if direction_y > 0:  # Moving down
                    self.rect.bottom = solid_tile.top
                if direction_y < 0:  # Moving up
                    self.rect.top = solid_tile.bottom

        # Create a smaller collision rect for trees
        collision_rect = self.rect.inflate(-50, -50)  # Make this value smaller to allow closer approach

        # Prevent going off-screen
        self.rect.clamp_ip(pygame.Rect(0, 0, self.screen_width, self.screen_height))

        # Re-check collisions with the smaller collision rectangle
        for solid_tile in solid_tiles:
            if collision_rect.colliderect(solid_tile):
                # Handle collision with the smaller collision box
                self.rect = original_position  # Revert to original position
                break  # Exit after first collision

import pygame

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Keybindings dictionary
keybindings = {
    "move_up": pygame.K_w,
    "move_left": pygame.K_a,
    "move_down": pygame.K_s,
    "move_right": pygame.K_d,
    "shoot": pygame.K_SPACE
}

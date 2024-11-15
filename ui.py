import pygame

import score
from config import WIDTH, HEIGHT, screen

# Load weapon images
banana_icon = pygame.image.load("images/banana.png")
coconut_icon = pygame.image.load("images/coconut.png")
orange_icon = pygame.image.load("images/orange.png")
snowball_icon = pygame.image.load("images/snowball.png")
icon_size = (60, 60)

# Load the heart image
heart_image = pygame.image.load("images/heart.png")  # Adjust the path if necessary
heart_width = 40  # Desired width for each heart
heart_height = 40  # Desired height for each heart

# Resize the weapon icons
banana_icon = pygame.transform.scale(banana_icon, icon_size)
coconut_icon = pygame.transform.scale(coconut_icon, icon_size)

retro_font = 'fonts/PressStart2P-Regular.ttf'
color = "white"
background_color = "black"
rectangles = {}
game_start_time = 0  # Timer to track how long the game has been running


def draw_weapon_selection(available_weapons):
    y_pos = HEIGHT - 50  # Vertical position for icons
    x_pos = 50  # Initial horizontal position

    # Show the weapons based on the available_weapons list
    if "banana" in available_weapons:
        text_component(retro_font, 20, "1", "black", None, None, None, x_pos, y_pos, "banana_key")
        screen.blit(banana_icon, (x_pos, y_pos - 30))
        x_pos += 80  # Increment position for the next icon

    if "coconut" in available_weapons:
        text_component(retro_font, 20, "2", "black", None, None, None, x_pos, y_pos, "coconut_key")
        screen.blit(coconut_icon, (x_pos, y_pos - 30))
        x_pos += 80

    if "orange" in available_weapons:
        text_component(retro_font, 20, "3", "black", None, None, None, x_pos, y_pos, "orange_key")
        screen.blit(orange_icon, (x_pos, y_pos - 30))
        x_pos += 80

    if "snowball" in available_weapons:
        text_component(retro_font, 20, "1", "black", None, None, None, x_pos, y_pos, "snowball_key")
        screen.blit(snowball_icon, (x_pos, y_pos - 30))


def text_component(text_font, text_size, text_content, text_color, text_background_color,
                   hover_text_color=None, hover_bg_color=None, position_x=0.0, position_y=0.0, rectangle_name=""):
    font = pygame.font.Font(text_font, text_size)
    text = font.render(text_content, True, text_color, text_background_color)
    rectangles[rectangle_name] = text.get_rect()
    rectangles[rectangle_name].center = (position_x, position_y)

    # Check if hover effect should be applied
    if hover_text_color and hover_bg_color:
        mouse_pos = pygame.mouse.get_pos()
        if rectangles[rectangle_name].collidepoint(mouse_pos):
            text = font.render(text_content, True, hover_text_color, hover_bg_color)

    screen.blit(text, rectangles[rectangle_name])


def display_score_and_timer():
    # Calculate the elapsed time in seconds
    elapsed_time = (pygame.time.get_ticks() - game_start_time) // 1000  # Convert milliseconds to seconds

    # Calculate minutes and seconds
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60

    # Format the time as MM:SS (e.g., 02:34)
    time_string = f"{minutes:02}:{seconds:02}"

    # Display the score and timer at the top center of the screen
    text_component(retro_font, 16, f"Score: {score.points}", "white", background_color, None, None, WIDTH / 3, 40,
                   "score")
    text_component(retro_font, 16, f"Time: {time_string}", "white", background_color, None, None, 2 * WIDTH / 3, 40,
                   "timer")


def draw_health_bar(health):
    for i in range(health):
        # Calculate the position for each heart
        x = 40 + (i * (heart_width + 5))  # Adjust the spacing between hearts
        y = 20  # Fixed vertical position
        heart_resized = pygame.transform.scale(heart_image, (heart_width, heart_height))  # Resize the heart
        screen.blit(heart_resized, (x, y))  # Draw the heart on the screen

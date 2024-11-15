import random

import pygame

import audio
import config
import score
import ui
from audio import sfx_on, projectile_sound
from banana_animation import update_bananas, draw_bananas
from config import keybindings, WIDTH, HEIGHT, screen
from enemy import Toucan, Alligator, Penguin, Snowman
from map import place_trees, tiles_grass, tiles_snow, Map, grid
from player import Player
from projectile import Projectile
from save import save_game_data, load_game_data
from score import score_timer, check_high_score
from ui import draw_weapon_selection, text_component, display_score_and_timer, draw_health_bar, \
    retro_font, background_color, rectangles

pygame.init()
pygame.display.set_caption('Kong')
clock = pygame.time.Clock()

# Variables to limit player attack speed
last_shot_time = 0
projectile_cooldown = 400

# Randomly place trees in the grid
place_trees()

selected_map_tiles = None  # Initialize this variable
player = Player(WIDTH, HEIGHT, keybindings)

projectiles = []
projectile_type = "banana"


def start_screen():
    running = True
    load_game_data()
    audio.play_background_music()

    while running:
        screen.fill(background_color)

        # Update the positions of the bananas
        update_bananas()
        draw_bananas()

        # Use the new text_component function with hover effects
        text_component(retro_font, 148, "KONG", "white", "black", None, None, WIDTH / 2, HEIGHT / 3, "title")
        text_component(retro_font, 32, "START GAME", "white", background_color, "black", "white", WIDTH / 2,
                       HEIGHT / 1.7, "start_game")
        text_component(retro_font, 32, "OPTIONS", "white", background_color, "black", "white", WIDTH / 2, HEIGHT / 1.5,
                       "options")
        text_component(retro_font, 32, "EXIT", "white", background_color, "black", "white", WIDTH / 2, HEIGHT / 1.35,
                       "exit")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game_data()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if rectangles["start_game"].collidepoint(mouse_pos):
                    map_selection_screen()
                elif rectangles["options"].collidepoint(mouse_pos):
                    options_screen()
                elif rectangles['exit'].collidepoint(mouse_pos):
                    save_game_data()
                    running = False

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def map_selection_screen():
    global selected_map_tiles
    running = True

    while running:
        screen.fill(background_color)

        text_component(retro_font, 48, "SELECT MAP", "white", "black", None, None, WIDTH / 2, HEIGHT / 5, "map_title")
        text_component(retro_font, 32, "JUNGLE MAP", "white", background_color, "black", "white", WIDTH / 2,
                       HEIGHT / 2.5, "grass_map")
        text_component(retro_font, 32, "SNOW MAP", "white", background_color, "black", "white", WIDTH / 2, HEIGHT / 1.8,
                       "snow_map")
        text_component(retro_font, 32, "BACK", "white", background_color, "black", "white", WIDTH / 2, HEIGHT / 1.2,
                       "back")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game_data()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if rectangles["grass_map"].collidepoint(mouse_pos):
                    selected_map_tiles = tiles_grass  # Set selected map tiles to grass
                    main_game()
                elif rectangles["snow_map"].collidepoint(mouse_pos):
                    selected_map_tiles = tiles_snow  # Set selected map tiles to snow
                    main_game()
                elif rectangles["back"].collidepoint(mouse_pos):
                    start_screen()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def main_game():
    global projectiles
    global projectile_type
    global last_shot_time
    enemies = []

    load_game_data()

    score.points = 0  # Reset the score when the game starts
    ui.score_timer = pygame.time.get_ticks()  # Reset the timer
    ui.game_start_time = pygame.time.get_ticks()  # Track when the game starts
    # Set conditions based on selected map
    if selected_map_tiles == tiles_snow:
        allowed_enemies = [Penguin, Snowman]
        available_weapons = ["snowball"]
        projectile_type = "snowball"  # Set snowball as the only weapon
    else:  # Grass map
        allowed_enemies = [Toucan, Alligator]
        available_weapons = ["banana", "coconut", "orange"]

    player.rect.x = WIDTH // 2 - player.rect.width // 2
    player.rect.y = HEIGHT - player.rect.height - 10

    health = 3  # Number of hearts (health)

    running = True

    audio.stop_background_music()

    screen.fill(background_color)

    # Create the tile map using the selected map tiles
    tile_map = Map(grid, selected_map_tiles)  # Use selected_map_tiles here
    tile_map.load()

    # Initialize spawn timer
    spawn_timer = pygame.time.get_ticks()
    spawn_interval = 2500

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    start_screen()
                elif event.key == pygame.K_END:
                    end_screen()
                elif event.key == pygame.K_1 and "banana" in available_weapons:
                    projectile_type = "banana"
                elif event.key == pygame.K_2 and "coconut" in available_weapons:
                    projectile_type = "coconut"
                elif event.key == pygame.K_3 and "orange" in available_weapons:
                    projectile_type = "orange"
                elif event.key == pygame.K_4 and "snowball" in available_weapons:
                    projectile_type = "snowball"
                elif event.type == pygame.KEYDOWN:
                    if event.key == keybindings['shoot']:
                        current_time = pygame.time.get_ticks()
                        if current_time - last_shot_time >= projectile_cooldown:
                            projectile = Projectile(player.rect.x, player.rect.y, projectile_type)
                            projectiles.append(projectile)
                            last_shot_time = current_time
                            if sfx_on:
                                projectile_sound.play()

        # Check if 10 seconds (10,000 milliseconds) have passed to increase the score
        if pygame.time.get_ticks() - score_timer >= 10000:
            score.points += 1
            ui.score_timer = pygame.time.get_ticks()  # Reset the timer

        # Spawn new enemies based on allowed types for the selected map
        if pygame.time.get_ticks() - spawn_timer >= spawn_interval:
            enemy_type = random.choice(allowed_enemies)
            new_enemy = enemy_type(x=random.randint(0, WIDTH - 50), y=-50, screen_width=WIDTH, screen_height=HEIGHT)
            enemies.append(new_enemy)
            spawn_timer = pygame.time.get_ticks()  # Reset the spawn timer

        player.move(tile_map.solid_tiles)

        # Enemy follows the player
        for enemy in enemies:
            enemy.follow(player.rect)
            if enemy.rect.colliderect(player.rect) and enemy.alive:
                health -= 1
                enemy.alive = False
                if health == 0:
                    end_screen()

        # Update projectiles and check for enemy collisions
        for projectile in projectiles:
            projectile.update()
            for enemy in enemies:
                if enemy.alive and projectile.rect.colliderect(enemy.rect):
                    if enemy.health == 0:
                        enemy.alive = False
                        if sfx_on:
                            audio.enemy_death_sound.play()
                        score.points += 1
                    else:
                        enemy.health -= 1
                    projectiles.remove(projectile)
                    break

        # Update projectiles list and screen drawing
        projectiles = [projectile for projectile in projectiles if not projectile.is_off_screen()]
        screen.fill(background_color)
        tile_map.draw(screen)
        for enemy in enemies:
            if enemy.alive:
                enemy.draw(screen)
        for projectile in projectiles:
            projectile.draw(screen)
        display_score_and_timer()
        draw_health_bar(health)
        screen.blit(player.image, player.rect)
        draw_weapon_selection(available_weapons)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def options_screen():
    running = True
    rebinding = None  # Keeps track of whether the player is rebinding a key

    while running:
        screen.fill(background_color)

        # Display the options title
        text_component(retro_font, 48, "OPTIONS", "white", "black", None, None, WIDTH / 2, HEIGHT / 5, "options")

        # Display "TOGGLE MUSIC" with its ON/OFF status
        music_status = "ON" if audio.music_on else "OFF"
        text_component(retro_font, 24, f"TOGGLE MUSIC ({music_status})", "white", "black", "black", "white", WIDTH / 2,
                       HEIGHT / 3, "toggle_music")

        # Display "TOGGLE SFX" with its ON/OFF status
        sfx_status = "ON" if audio.sfx_on else "OFF"
        text_component(retro_font, 24, f"TOGGLE SFX ({sfx_status})", "white", "black", "black", "white", WIDTH / 2,
                       HEIGHT / 2.5, "toggle_sfx")

        # Display the current key bindings
        text_component(retro_font, 24, f"MOVE UP: {pygame.key.name(config.keybindings['move_up']).upper()}", "white",
                       "black",
                       "black", "white", WIDTH / 2, HEIGHT / 2.2, "move_up")
        text_component(retro_font, 24, f"MOVE LEFT: {pygame.key.name(config.keybindings['move_left']).upper()}",
                       "white",
                       "black", "black", "white", WIDTH / 2, HEIGHT / 2, "move_left")
        text_component(retro_font, 24, f"MOVE DOWN: {pygame.key.name(config.keybindings['move_down']).upper()}",
                       "white",
                       "black", "black", "white", WIDTH / 2, HEIGHT / 1.8, "move_down")
        text_component(retro_font, 24, f"MOVE RIGHT: {pygame.key.name(config.keybindings['move_right']).upper()}",
                       "white",
                       "black", "black", "white", WIDTH / 2, HEIGHT / 1.6, "move_right")
        text_component(retro_font, 24, f"SHOOT: {pygame.key.name(config.keybindings['shoot']).upper()}", "white",
                       "black",
                       "black", "white", WIDTH / 2, HEIGHT / 1.4, "shoot")

        # Display the "BACK" option
        text_component(retro_font, 32, "BACK", "white", "black", "black", "white", WIDTH / 2, HEIGHT / 1.2, "back")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game_data()
                running = False
            if event.type == pygame.KEYDOWN:
                if rebinding:
                    # If we're in the rebinding state, capture the pressed key
                    config.keybindings[rebinding] = event.key
                    rebinding = None  # Exit rebinding state
                    save_game_data()
                elif event.key == pygame.K_BACKSPACE:
                    start_screen()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if rectangles["back"].collidepoint(mouse_pos):
                    start_screen()
                elif rectangles["toggle_music"].collidepoint(mouse_pos):
                    audio.toggle_music()
                    save_game_data()
                elif rectangles["toggle_sfx"].collidepoint(mouse_pos):
                    audio.toggle_sfx()
                    save_game_data()

                # If the player clicks on a keybinding option, enter rebinding state
                if rectangles["move_up"].collidepoint(mouse_pos):
                    rebinding = "move_up"
                elif rectangles["move_left"].collidepoint(mouse_pos):
                    rebinding = "move_left"
                elif rectangles["move_down"].collidepoint(mouse_pos):
                    rebinding = "move_down"
                elif rectangles["move_right"].collidepoint(mouse_pos):
                    rebinding = "move_right"
                elif rectangles["shoot"].collidepoint(mouse_pos):
                    rebinding = "shoot"

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def end_screen():
    running = True

    # Reset the game_start_time to restart the timer
    ui.game_start_time = 0  # Reset the timer here

    check_high_score()

    while running:
        screen.fill(background_color)

        # Display the game over message and options
        text_component(retro_font, 64, "GAME OVER", "red", "black", None, None, WIDTH / 2, HEIGHT / 2.3, "game_over")
        text_component(retro_font, 32, "PLAY AGAIN?", "white", "black", None, None, WIDTH / 2, HEIGHT / 1.8,
                       "play_again")
        text_component(retro_font, 20, "YES", "white", "black", "black", "white", WIDTH / 2.45, HEIGHT / 1.55, "yes")
        text_component(retro_font, 20, "NO", "white", "black", "black", "white", WIDTH / 1.65, HEIGHT / 1.55, "no")

        # Display "HIGH SCORE" in the top-middle and the actual high score below it (Text in blue, score in white)
        text_component(retro_font, 25, "HIGH SCORE", "#3890D8", "black", None, None, WIDTH / 2, HEIGHT / 9,
                       "high_score_label")
        text_component(retro_font, 25, f"{score.high_score}", "white", "black", None, None, WIDTH / 2, HEIGHT / 5.6,
                       "high_score_value")

        # Display "YOUR SCORE" in the bottom-left (Text in blue, score in white)
        text_component(retro_font, 25, "YOUR SCORE:", "#3890D8", "black", None, None, WIDTH / 5, HEIGHT - 60,
                       "your_score_label")
        text_component(retro_font, 25, f"{score.points}", "white", "black", None, None, WIDTH / 2.3, HEIGHT - 60,
                       "your_score_value")

        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game_data()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    start_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rectangles["yes"].collidepoint(mouse_pos):
                    main_game()
                elif rectangles["no"].collidepoint(mouse_pos):
                    running = False

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


start_screen()

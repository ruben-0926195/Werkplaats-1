import pygame

pygame.mixer.init()

background_music = 'sounds/8-bit-heaven.mp3'
projectile_sound = pygame.mixer.Sound('sounds/8-bit-laser.mp3')
enemy_death_sound = pygame.mixer.Sound('sounds/retro-coin-1-236677.mp3')

music_on = True
sfx_on = True


def play_background_music():
    # Only play the music if the music is turned on
    if music_on and not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(background_music)
        pygame.mixer.music.play(-1, 0.0)


def stop_background_music():
    pygame.mixer.music.stop()


def play_projectile_sound():
    if sfx_on:
        projectile_sound.play()


def play_enemy_death_sound():
    if sfx_on:
        enemy_death_sound.play()


def toggle_music():
    global music_on
    if music_on:
        stop_background_music()
    else:
        play_background_music()
    music_on = not music_on


def toggle_sfx():
    global sfx_on
    sfx_on = not sfx_on

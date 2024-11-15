import json

import pygame

import audio
import config
import score

default_data = {
    "high_score": 0,
    "keybindings": {
        "move_up": pygame.K_w,
        "move_left": pygame.K_a,
        "move_down": pygame.K_s,
        "move_right": pygame.K_d,
        "shoot": pygame.K_SPACE
    },
    "sfx_on": True,
    "music_on": True
}


# Saves the high score to an external file creates on if none is found
def save_game_data():
    data = {
        "high_score": score.high_score,
        "keybindings": config.keybindings,
        "sfx_on": audio.sfx_on,
        "music_on": audio.music_on
    }
    with open('save_data.json', 'w') as file:
        json.dump(data, file)


def load_game_data():
    try:
        with open('save_data.json', 'r') as file:
            data = json.load(file)
            score.high_score = data.get("high_score", 0)
            config.keybindings = data.get("keybindings", config.keybindings)
            audio.sfx_on = data.get("sfx_on", True)
            audio.music_on = data.get("music_on", True)
    except FileNotFoundError:
        # File does not exist, create it with default values
        with open('save_data.json', 'w') as file:
            json.dump(default_data, file)
        score.high_score = default_data["high_score"]
        config.keybindings = default_data["keybindings"]
        audio.sfx_on = default_data["sfx_on"]
        audio.music_on = default_data["music_on"]

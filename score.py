from save import save_game_data

score_timer = 0  # Timer to track when to increment the score (in milliseconds)
high_score = 0  # Global variable to store the high score
points = 0  # Score variable and time tracking


def check_high_score():
    global high_score
    if points > high_score:
        high_score = points
        save_game_data()

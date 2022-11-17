import string
import random

game_lists = {}

def random_string(length):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))

class GameInfo:
    def __init__(self):
        self.start_token = None

def create_game():
    game = GameInfo()
    game.id = random_string(6)
    game.start_token = random_string(64)
    game_lists[game.id] = game
    return game

def get_game_info(game_id):
    if game_id in game_lists:
        return game_lists[game_id]
    else:
        return None
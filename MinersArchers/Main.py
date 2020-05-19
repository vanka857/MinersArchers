import json

from game.Game import Game
from static import config_path

with open(config_path("field.json"), "r") as read_file:
    json_field = json.load(read_file)

w = json_field["W_IN_CELLS"]
h = json_field["H_IN_CELLS"]

game = Game(w, h, "py_game")
print("")
game.start()


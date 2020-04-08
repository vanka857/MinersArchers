import pygame
from .Dispatcher import Dispatcher


class PyGameDispatcher(Dispatcher):

    def __init__(self, py_game_):
        super().__init__()
        self.py_game = py_game_
        print('PyGame Dispatcher created!')

    def check_new_commands(self) -> 'has_new_commands, commands':
        return self.py_game.check_new_commands()

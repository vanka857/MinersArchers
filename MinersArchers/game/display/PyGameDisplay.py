from game.display.Display import Display
from game.game_data.PyGame import PyGame
import pygame


class PyGameDisplay(Display):

    def __init__(self, py_game_, w, h):
        super().__init__()
        py_game_.init_screen(w, h)
        self._screen = py_game_.get_screen()
        self.py_game = py_game_
        print('PyGame Display created!')

    def get_screen(self):
        return self.py_game.get_screen()

    def update(self):
        self.py_game.draw()
        print('Display updated')

    def set_data(self, data):
        self.py_game.set_field_data(data)

    def wait(self, time=50):
        self.py_game.wait(time)



import pygame

from game.logs.Logs import Logs

log = Logs()

# размер одной ячейки(квадратной) в пикселях
CELL_SIZE = 200
UNIT_SIZE = 100

CELL_HEIGHT = CELL_SIZE
CELL_WIDTH = CELL_SIZE

UNIT_HEIGHT = CELL_HEIGHT / 2
UNIT_WIDTH = CELL_WIDTH / 2


def get_object_on_coords(x, y):
    # вводим ккординаты на нашем поле
    y_field = int(y / CELL_HEIGHT)
    x_field = int(x / CELL_WIDTH)
    # теперь мы знаем, какой cell, узнаем, попали в unit или нет
    if (x_field + 1 / 4) * CELL_WIDTH < x < (x_field + 3 / 4) * CELL_WIDTH:
        if (y_field + 1 / 4) * CELL_HEIGHT < y < (y_field + 3 / 4) * CELL_HEIGHT:
            return (y_field, x_field), "unit"
    return (y_field, x_field), "cell"


# класс, где реализован ввод + ввывод + обработка некоторых команд на pygame
class PyGame:

    def __init__(self):
        pygame.init()
        # просто создаем переменную
        self.__screen = None
        log.print("PyGame initialized")

    def init_screen(self, w, h):
        self.__screen = pygame.display.set_mode((w, h))

    def get_screen(self):
        return self.__screen

    def update_display(self):
        # Flip the display
        pygame.display.flip()

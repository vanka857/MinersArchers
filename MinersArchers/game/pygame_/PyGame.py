import pygame

from game.logs.Logs import Logs

log = Logs()

# размер одной ячейки(квадратной) в пикселях
CELL_SIZE = 202
UNIT_SIZE = 100

CELL_HEIGHT = CELL_SIZE
CELL_WIDTH = CELL_SIZE

UNIT_HEIGHT = UNIT_SIZE
UNIT_WIDTH = UNIT_SIZE

# словарь с картинками
PICS = {"mines": "pics/Mine.png",
        "barrack": "pics/Barrack.png",
        "cell1": "pics/Valley.png",
        "cell2": "pics/Mountain.png",
        "archers": "pics/Archer.png",
        "warriors": "pics/Warrior.png",
        "miners": "pics/Miner.png",
        "unit_frame": "pics/Frame_unit.png",
        "cell_frame": "pics/Frame_cell.png",
        "action": "pics/Frame_cell.png",
        "button": "pics/button.png",
        "buttonHovered": "pics/buttonHovered.png",
        "buttonSelected": "pics/buttonSelected.png",
        "emblem0": "pics/Emblem0.png",
        "emblem1": "pics/Emblem1.png",
        "coins": "pics/Coins.png"}


# класс, где реализован ввод + ввывод + обработка некоторых команд на pygame_
class PyGame:

    def __init__(self):
        pygame.init()
        # просто создаем переменную
        self.__screen = None

        self.w = None
        self.h = None
        log.mprint("PyGame initialized")

    def init_screen(self, w, h):
        self.w = w
        self.h = h
        self.__screen = pygame.display.set_mode((w, h))

    def get_screen(self):
        return self.__screen

    def update_display(self):
        # Flip the display
        pygame.display.flip()

    def get_object_on_coords(self, x, y):
        # вводим ккординаты на нашем поле
        y_field = int(y / CELL_HEIGHT)
        x_field = int(x / CELL_WIDTH)
        # теперь мы знаем, какой cell, узнаем, попали в unit или нет

        # если нажали правее или ниже игрового поля
        if x_field >= int(self.w / CELL_WIDTH):
            return None
        if y_field >= int(self.h / CELL_HEIGHT):
            return None

        # если нажали на что-то в последнем стоблике, значит, это команда
        if x_field == int(self.w / CELL_SIZE) - 1:
            return (y_field, x_field), "action"

        # иначе определяем cell это или unit
        if x_field * CELL_WIDTH + (CELL_WIDTH - UNIT_WIDTH) / 2 < x < x_field * CELL_WIDTH + \
                UNIT_WIDTH + (CELL_WIDTH - UNIT_WIDTH) / 2:
            if y_field * CELL_HEIGHT + (CELL_HEIGHT - UNIT_HEIGHT) / 2 < y < y_field * CELL_HEIGHT \
                    + UNIT_HEIGHT + (CELL_HEIGHT - UNIT_HEIGHT) / 2:
                return (y_field, x_field), "unit"

        return (y_field, x_field), "cell"

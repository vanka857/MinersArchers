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
PICS_pygame = {"mines": "pics/Mine.png",
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


# Этот код выполняется при импорте модуля pygame_ (не класса! Класса "нашего" PyGame больше нет)

pygame.init()
# просто создаем переменную
__screen = None

w = None
h = None
log.mprint("PyGame initialized")


# это просто набор наших функций для работы с pygame

def init_screen(w_, h_):
    global w, h
    w = w_
    h = h_
    return pygame.display.set_mode((w_, h_))


def update_display():
    # Flip the display
    pygame.display.flip()


def get_object_on_coords(x, y):
    # вводим ккординаты на нашем поле
    y_field = int(y / CELL_HEIGHT)
    x_field = int(x / CELL_WIDTH)
    # теперь мы знаем, какой cell, узнаем, попали в unit или нет

    global w, h
    # если нажали правее или ниже игрового поля
    if x_field >= int(w / CELL_WIDTH):
        return None
    if y_field >= int(h / CELL_HEIGHT):
        return None

    # если нажали на что-то в последнем стоблике, значит, это команда
    if x_field == int(w / CELL_SIZE) - 1:
        return (y_field, x_field), "action"

    # иначе определяем cell это или unit
    if x_field * CELL_WIDTH + (CELL_WIDTH - UNIT_WIDTH) / 2 < x < x_field * CELL_WIDTH + \
            UNIT_WIDTH + (CELL_WIDTH - UNIT_WIDTH) / 2:
        if y_field * CELL_HEIGHT + (CELL_HEIGHT - UNIT_HEIGHT) / 2 < y < y_field * CELL_HEIGHT \
                + UNIT_HEIGHT + (CELL_HEIGHT - UNIT_HEIGHT) / 2:
            return (y_field, x_field), "unit"

    return (y_field, x_field), "cell"

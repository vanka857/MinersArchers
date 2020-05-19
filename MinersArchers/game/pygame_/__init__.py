import pygame

from game.logs.Logs import Logs
from static import config_path, resource_path
import json

log = Logs()

with open(config_path("field.json"), "r") as read_file:
    field = json.load(read_file)

# размер одной ячейки(квадратной) в пикселях
CELL_SIZE = field["CELL_SIZE"]
UNIT_SIZE = field["UNIT_SIZE"]

CELL_HEIGHT = CELL_SIZE
CELL_WIDTH = CELL_SIZE

UNIT_HEIGHT = UNIT_SIZE
UNIT_WIDTH = UNIT_SIZE

# словарь с картинками
PICS_pygame = {}
PICS_pygame["mines"] = resource_path("pics/Mine.png")
PICS_pygame["barrack"] = resource_path("pics/Barrack.png")
PICS_pygame["cell1"] = resource_path("pics/Valley.png")
PICS_pygame["cell2"] = resource_path("pics/Mountain.png")
PICS_pygame["archers"] = resource_path("pics/Archer.png")
PICS_pygame["warriors"] = resource_path("pics/Warrior.png")
PICS_pygame["miners"] = resource_path("pics/Miner.png")
PICS_pygame["unit_frame"] = resource_path("pics/Frame_unit.png")
PICS_pygame["cell_frame"] = resource_path("pics/Frame_cell.png")
PICS_pygame["action"] = resource_path("pics/Frame_cell.png")
PICS_pygame["button"] = resource_path("pics/button.png")
PICS_pygame["buttonHovered"] = resource_path("pics/buttonHovered.png")
PICS_pygame["buttonSelected"] = resource_path("pics/buttonSelected.png")
PICS_pygame["emblem0"] = resource_path("pics/Emblem0.png")
PICS_pygame["emblem1"] = resource_path("pics/Emblem1.png")
PICS_pygame["coins"] = resource_path("pics/Coins.png")

# PICS_pygame = {"mines": resource_path("static/pics/Mine.png"),
#                "barrack": resource_path("static/pics/Barrack.png"),
#                "cell1": resource_path("static/pics/Valley.png"),
#                "cell2": resource_path("static/pics/Mountain.png"),
#                "archers": resource_path("static/pics/Archer.png"),
#                "warriors": resource_path("static/pics/Warrior.png"),
#                "miners": resource_path("static/pics/Miner.png"),
#                "unit_frame": resource_path("static/pics/Frame_unit.png"),
#                "cell_frame": resource_path("static/pics/Frame_cell.png"),
#                "action": resource_path("static/pics/Frame_cell.png"),
#                "button": resource_path("static/pics/button.png"),
#                "buttonHovered": resource_path("static/pics/buttonHovered.png"),
#                "buttonSelected": resource_path("static/pics/buttonSelected.png"),
#                "emblem0": resource_path("static/pics/Emblem0.png"),
#                "emblem1": resource_path("static/pics/Emblem1.png"),
#                "coins": resource_path("static/pics/Coins.png")}


# Этот код выполняется при импорте модуля pygame_ (не класса! Класса "нашего" PyGame больше нет)

pygame.init()
# просто создаем переменную
__screen = None

w = None
h = None
log.mprint("PyGame initialized")


font_family = resource_path("fonts/Comic_Sans_MS.ttf")  # Hard-code a local path


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
    # если нажали правее или ниже игрового п_objectоля
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

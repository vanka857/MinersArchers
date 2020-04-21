# coding=utf-8

import pygame

from game.display.Display import Display
from game.game_data import PyGame
from game.logs.Logs import Logs

# устанавливаем цвет логов
log = Logs("Yellow")

# размер одной ячейки(квадратной) в пикселях
CELL_SIZE = PyGame.CELL_SIZE
UNIT_SIZE = PyGame.UNIT_SIZE

TOOLBAR_HEIGHT = 70

PICS = {"mines"    : "pics/Mine.png",
        "barrack"  : "pics/Barrack.png",
        0          : "pics/Valley.png",
        1          : "pics/Mountain.png",
        "archers"  : "pics/Archer.png",
        "warriors" : "pics/Warrior.png",
        "miners"   : "pics/Miner.png",
        "unit"     : "pics/Frame_unit.png",
        "cell"     : "pics/Frame_cell.png",
        "action"   : "pics/Frame_cell.png",
        "button": "pics/button.png",
        "buttonHovered": "pics/buttonHovered.png",
        "buttonSelected": "pics/buttonSelected.png",}

class PyGCells:

    def __init__(self, cells):
        n = 0

        self.cells = list()
        self.cell_id_on_coord = dict()

        for i in range(len(cells)):
            for j in range(len(cells[i])):
                # create PyGCell from cell[i][j] (class game_data.Cell)
                # and append it to self.cells (class PyGCell)
                # меняем координаты местами. Так удобнее будет в pygame.
                # Сначала позиция по горизонтали(ширине),
                # потом - по вертикали(высоте)
                pyg_cell = PyGCell(cells[i][j], n, j, i)
                self.cells.append(pyg_cell)
                # меняем координаты местами. Так удобнее будет в pygame.
                # Сначала позиция по горизонтали(ширине),
                # потом - по вертикали(высоте)
                self.cell_id_on_coord[(j, i)] = n
                n += 1

    def create_coord_for_cell(self, x, y):
        return CELL_SIZE * x, CELL_SIZE * y

    def render(self, dest):
        for pyg_cell in self.cells:
            dest.blit(pyg_cell.surf, self.create_coord_for_cell(pyg_cell.x, pyg_cell.y))


class PyGCell(pygame.sprite.Sprite):
    def __init__(self, cell, id__, x_, y_):
        self.id_ = id__
        self.x = x_
        self.y = y_
        super().__init__()
        self.surf = pygame.Surface((CELL_SIZE, CELL_SIZE))

        # пока что расставляем текстуры в шахматном порядке
        internal = pygame.image.load(PICS[(self.x + self.y) % 2]).convert_alpha()

        self.surf.blit(internal, (CELL_SIZE * 0, CELL_SIZE * 0))
        self.rect = self.surf.get_rect()


class PyGUnits:

    def __init__(self, units):
        n = 0

        self.units = list()
        self.units_id_on_coord = dict()

        # перевод словаря из юнитов из game_data в двмумерный список
        for (i_, j_) in units.keys():
            unit = units[(i_, j_)]
            pyg_unit = PyGUnit(unit, j_, i_, unit.level, n)

            self.units.append(pyg_unit)
            self.units_id_on_coord[(j_, i_)] = pyg_unit
            n += 1

    def create_coord_for_unit(self, x, y):
        return CELL_SIZE * x + (CELL_SIZE - UNIT_SIZE) / 2, CELL_SIZE * y + (CELL_SIZE - UNIT_SIZE) / 2

    def render(self, dest):
        for pyg_unit in self.units:
            dest.blit(pyg_unit.surf, self.create_coord_for_unit(pyg_unit.x, pyg_unit.y))


class PyGUnit(pygame.sprite.Sprite):

    def __init__(self, unit, x_, y_, level, id__):
        self.id_ = id__
        self.level = level
        self.x = x_
        self.y = y_
        super().__init__()
        self.surf = pygame.Surface((UNIT_SIZE, UNIT_SIZE), flags=pygame.SRCALPHA)
        self.surf.fill(0)

        if self.level == 0:
            internal = pygame.Surface((UNIT_SIZE, UNIT_SIZE), flags=pygame.SRCALPHA)
            internal.fill(0)
        else:
            internal = pygame.image.load(PICS[unit.type]).convert_alpha()

        self.surf.blit(internal, (UNIT_SIZE * 0, UNIT_SIZE * 0))

        if unit.player != "died":
            f1 = pygame.font.Font(None, 28)
            text_level = f1.render('HP:{}'.format(unit.get_level()), 1, (0, 0, 0))
            self.surf.blit(text_level, (UNIT_SIZE * 0.1, UNIT_SIZE * 0.8))


# кнопкиииииии
av_but_com = {0: "attack", 1: "move", 2: "create", 3: "upgrade"} # 3: "build",# 4: "upgrade"}


class PyGButtons(pygame.sprite.Sprite):
    def __init__(self):
        self.buttons = list()
        button = pygame.image.load(PICS["button"]).convert_alpha()
        buttonH = pygame.image.load(PICS["buttonHovered"]).convert_alpha()
        buttonS = pygame.image.load(PICS["buttonSelected"]).convert_alpha()

        for i in range(len(av_but_com)):
            self.buttons.append(
                Button(0, i * CELL_SIZE, CELL_SIZE, CELL_SIZE, button, buttonH, buttonS, av_but_com[i]))

    def render(self, dest):
        for i in range(self.buttons.__len__()):
            self.buttons[i].draw(dest, i)


class Button:
    def __init__(self, x, y, width, height, image, hovered_image, selected_image, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = image
        self.hovered_image = hovered_image
        self.selected_image = selected_image
        self.selected = False
        self.hovered = False

    def draw(self, surface, i):

        # surface.fill((255,255,255,255))

        if self.selected:
            surface.blit(self.selected_image, (0, CELL_SIZE * i))

        elif self.hovered:
            surface.blit(self.hovered_image, (0, CELL_SIZE * i))

        else:
            surface.blit(self.image, (0, CELL_SIZE * i))

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, 1, (77, 77, 77))
            surface.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2),
            self.y + (self.height / 2 - text.get_height() / 2)))


class PyGBuilding(pygame.sprite.Sprite):
    pass

class PyGameDisplay(Display):

    def __init__(self, py_game_, w, h, queue=None):
        super().__init__()
        self.data = None
        self.queue = queue
        self.py_game = py_game_
        # столбец для кнопок
        self.field_w = w * CELL_SIZE
        self.field_h = h * CELL_SIZE
        self.xCells = w
        self.yCells = h
        self.w = (w + 1) * CELL_SIZE
        self.h = h * CELL_SIZE + TOOLBAR_HEIGHT
        self.py_game.init_screen(self.w, self.h)
        self.screen = self.py_game.get_screen()

        self.__field_layer = None
        self.__units_layer = None
        self.__buttons_layer = None
        self.__toolbar_layer = None
        self.__frame_layer = None
        self.__buildings_layer = None

        self.pyg_cells = None
        self.pyg_units = None
        self.pyg_buttons = None
        self.pyg_buildings = None

        self.field_created = False

        log.mprint('PyGame Display created!')

    # как раз тут все данные из game_data, с которыми взаимодействует контроллер
    def set_data(self, data):
        self.data = data

    def get_screen(self):
        return self.py_game.get_screen()

    redraw_buttons = False

    def update(self):

        if not self.field_created:
            self.field_created = True
            self.draw("all")

        def positions_to_blit(x_, y_):
            return {"unit": (CELL_SIZE * x_ + (CELL_SIZE - UNIT_SIZE) / 2, CELL_SIZE * y_ + (CELL_SIZE - UNIT_SIZE) / 2),
                    "cell": (x_ * CELL_SIZE, y_ * CELL_SIZE),
                    "action": (x_ * CELL_SIZE, y_ * CELL_SIZE)}

        bordered_y = None
        bordered_x = None
        bordered_type = None

        hovered_button = None
        selected_button = None

        while len(self.queue) > 0:

            command = self.queue[0]

            log.mprint('got some commands: ' + str(command))

            if command[0] == "select":
                if command[1][1] == "action":
                    selected_button = command[1][0][0]
                    self.redraw_buttons = True
                else:
                    bordered_y = int(command[1][0][0])
                    bordered_x = int(command[1][0][1])
                    bordered_type = command[1][1]

            if command[0] == "hover":
                if command[1][1] == "action":
                    self.redraw_buttons = True
                    hovered_button = command[1][0][0]

            self.queue.popleft()

        if selected_button is not None:
            self.pyg_buttons.buttons[selected_button].selected = True
        if hovered_button is not None:
            self.pyg_buttons.buttons[hovered_button].hovered = True

        if self.redraw_buttons:
            self.redraw_buttons = False
            self.draw("buttons")

        if selected_button is not None:
            self.redraw_buttons = True
            self.pyg_buttons.buttons[selected_button].selected = False
        if hovered_button is not None:
            self.redraw_buttons = True
            self.pyg_buttons.buttons[hovered_button].hovered = False

        if bordered_type is not None:
            self.draw("frame")
            frame = pygame.image.load(PICS[bordered_type]).convert_alpha()
            self.__frame_layer.blit(frame, positions_to_blit(bordered_x, bordered_y)[bordered_type])

        # self.screen.fill((255, 255, 255, 255))
        self.screen.blit(self.__field_layer, (0, 0))
        self.screen.blit(self.__units_layer, (0, 0))
        self.screen.blit(self.__buttons_layer, (CELL_SIZE * self.xCells, 0))
        self.screen.blit(self.__frame_layer, (0, 0))
        self.screen.blit(self.__toolbar_layer, (0, self.field_h))

        self.py_game.update_display()
        # log.mprint('Display updated')


    def draw(self, *args):
        if "all" in args:
            self.create_field_layer()
            self.create_units_layer()
            self.create_buttons_layer()
            self.create_frame_layer()
            self.create_toolbar_layer()
        if "units" in args:
            self.create_units_layer()
        if "frame" in args:
            self.create_frame_layer()
        if "buttons" in args:
            self.create_buttons_layer()

    def create_frame_layer(self):
        if self.__frame_layer is None:
            self.__frame_layer = pygame.Surface((self.field_w, self.field_h), pygame.SRCALPHA, 32)
        else:
            self.__frame_layer.fill(0)

    def create_units_layer(self):
        if self.data is None:
            raise Exception
        # создание слоя из юнитов
        self.pyg_units = PyGUnits(self.data.units)
        if self.__units_layer is None:
            self.__units_layer = pygame.Surface((self.field_w, self.field_h), pygame.SRCALPHA, 32)

        self.__units_layer.fill(0)

        # их отрисовка
        self.pyg_units.render(self.__units_layer)

    def create_buttons_layer(self):
        # создание слоя из кнопок
        if self.__buttons_layer is None:
            self.pyg_buttons = PyGButtons()
            self.__buttons_layer = pygame.Surface((CELL_SIZE, self.field_h))

        self.__buttons_layer.fill((228, 213, 126))

        # их отрисовка
        self.pyg_buttons.render(self.__buttons_layer)

    def create_field_layer(self):
        if self.data is None:
            raise Exception
        # создание слоя из cell
        self.pyg_cells = PyGCells(self.data._cells)
        self.__field_layer = pygame.Surface((self.field_w, self.field_h))
        # их отрисовка
        self.pyg_cells.render(self.__field_layer)

    def create_toolbar_layer(self):
        if self.__toolbar_layer is None:
            self.__toolbar_layer = pygame.Surface((self.w, TOOLBAR_HEIGHT))

        self.__toolbar_layer.fill((228, 213, 126))

        # здесь должен быть вывод на слой информации

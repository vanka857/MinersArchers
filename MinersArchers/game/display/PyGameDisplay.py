# coding=utf-8

import pygame

from game.display.Display import Display
from game.game_data import PyGame
from game.game_data.units import Units
from game.logs.Logs import Logs

# устанавливаем цвет логов
log = Logs("Yellow")

# размер одной ячейки(квадратной) в пикселях
CELL_SIZE = PyGame.CELL_SIZE
UNIT_SIZE = PyGame.UNIT_SIZE

TOOLBAR_HEIGHT = 70
COLOR = (100, 100, 100)
RED = (200, 0, 0)
# словарь с картинками
PICS = {"mines": "pics/Mine.png",
        "barrack": "pics/Barrack.png",
        0: "pics/Valley.png",
        1: "pics/Mountain.png",
        "archers": "pics/Archer.png",
        "warriors": "pics/Warrior.png",
        "miners": "pics/Miner.png",
        "unit": "pics/Frame_unit.png",
        "cell": "pics/Frame_cell.png",
        "action": "pics/Frame_cell.png",
        "button": "pics/button.png",
        "buttonHovered": "pics/buttonHovered.png",
        "buttonSelected": "pics/buttonSelected.png",
        "emblem0": "pics/Emblem0.png",
        "emblem1": "pics/Emblem1.png",
        "coins": "pics/Coins.png"}


# новый родительский класс для Button PyGUnit и PyGCell
class Object(pygame.sprite.Sprite):
    def __init__(self, id, x, y, width, height, image):
        # инициализация базового класса
        super().__init__()
        # load image...
        self._id = id
        # эти в пикселях
        self._y_pix = y
        self._x_pix = x

        self._height = height
        self._width = width
        self._image = image

        self.surf = None
        self.rect = None

    def get_coords(self):
        return self._x_pix, self._y_pix

    def get_size(self):
        return self._width, self._height

    # создание картинки
    def load_image(self):
        self.surf = pygame.Surface((self._height, self._width), flags=pygame.SRCALPHA)

        internal = pygame.image.load(PICS[self._image]).convert_alpha()

        self.surf.blit(internal, (0, 0))
        self.rect = self.surf.get_rect()

    def draw(self, surface, pos=None):
        self.load_image()
        if not pos:
            pos = (self._x_pix, self._y_pix)

        surface.blit(self.surf, pos)


class PyGCell(Object):
    # в этот момент свапаем координаты
    def __init__(self, cell, y_, x_, id__):
        super().__init__(id__, self.create_coord(x_, y_)[0], self.create_coord(x_, y_)[1], CELL_SIZE, CELL_SIZE, 1)

    def create_coord(self, x, y):
        return CELL_SIZE * x, CELL_SIZE * y


class PyGUnit(Object, Units.Unit):
    def __init__(self, unit, id__):
        # на этом моменте свапаем координаты
        # инициализация Object
        Object.__init__(self, id__, self.create_coord(unit.get_cords()[1], unit.get_cords()[0])[0],
                        self.create_coord(unit.get_cords()[1], unit.get_cords()[0])[1], UNIT_SIZE, UNIT_SIZE, unit.type)

        # инициализация Unit
        Units.Unit.__init__(self, unit.get_player(), unit.get_level(), unit.get_type(),
                            unit.get_cords()[0], unit.get_cords()[1])

    def load_image(self):
        # в object это не реализовать, так как нужна информация о левеле и имени игрока
        self.surf = pygame.Surface((self._height, self._width), flags=pygame.SRCALPHA)

        if self.get_level() == 0:
            internal = pygame.Surface((UNIT_SIZE, UNIT_SIZE), flags=pygame.SRCALPHA)
            internal.fill(0)
        else:
            internal = pygame.image.load(PICS[self._image]).convert_alpha()

        self.surf.blit(internal, (0, 0))
        self.rect = self.surf.get_rect()

        if self.get_level() != 0:
            f1 = pygame.font.SysFont('comicsans', 28)
            text_level = f1.render('lvl:{}'.format(self.get_level()), 1, (50, 50, 50))
            text_name = f1.render('{}'.format(self.player), 1, (50, 50, 50))
            self.surf.blit(text_level, (UNIT_SIZE * 0.1 - 5, UNIT_SIZE * 0.8 - 7))
            self.surf.blit(text_name, (UNIT_SIZE * 0.6 - 5, UNIT_SIZE * 0.8 - 7))

    def create_coord(self, x, y):
        return CELL_SIZE * x + (CELL_SIZE - UNIT_SIZE) / 2, CELL_SIZE * y + (CELL_SIZE - UNIT_SIZE) / 2


class Group(pygame.sprite.Group):

    def __init__(self, new_objects=[]):
        super().__init__()
        self.objects = new_objects

    def add_object(self, new_object):
        self.objects.append(new_object)

    def update(self, differences):
        dif = self.getDif()

    # на вход приходит массив старых хэшей
    def get_dif(self, old_hash=[]):
        res = []
        for i in range(len(self.objects)):
            if self.objects[i].__hash__() != old_hash[i]:
                res.append(i)
        return res

    # отрисовка
    def render(self, dest):
        for obj in self.objects:
            obj.draw(dest)


class PyGCells(Group):
    def __init__(self, cells):
        n = 0
        self.cells = list()

        for (i, j) in cells.keys():
            pyg_cell = PyGCell(cells[(i, j)], i, j, n)
            self.cells.append(pyg_cell)
            n += 1
        # инициализация родительской Group
        Group.__init__(self, self.cells)


class PyGUnits(Group):
    def __init__(self, units):
        n = 0

        self.units = list()

        # перевод словаря из юнитов из game_data в двмумерный список
        for (i, j) in units.keys():
            unit = units[(i, j)]
            pyg_unit = PyGUnit(unit, n)

            self.units.append(pyg_unit)
            n += 1
        Group.__init__(self, self.units)

        if unit.player != "died":
            f1 = pygame.font.SysFont('comicsans', 28)
            text_level = f1.render('lvl:{}'.format(unit.get_level()), 1, (50, 50, 50))
            self.surf.blit(text_level, (UNIT_SIZE * 0.1 - 5, UNIT_SIZE * 0.8 - 7))

# кнопки
av_but_com = {0: "attack", 1: "move", 2: "create", 3: "upgrade"}


class PyGButtons(Group):
    def __init__(self):
        self.buttons = list()
        button = pygame.image.load(PICS["button"]).convert_alpha()
        buttonH = pygame.image.load(PICS["buttonHovered"]).convert_alpha()
        buttonS = pygame.image.load(PICS["buttonSelected"]).convert_alpha()

        for i in range(len(av_but_com)):
            self.buttons.append(
                Button(0, i * CELL_SIZE, CELL_SIZE, CELL_SIZE, button, buttonH, buttonS, av_but_com[i]))

        Group.__init__(self, self.buttons)


class Button(Object):
    def __init__(self, x, y, width, height, image, hovered_image, selected_image, text=''):
        Object.__init__(self, 0, x, y, width, height, image)
        self.text = text

        self.hovered_image = hovered_image
        self.selected_image = selected_image
        self.selected = False
        self.hovered = False

    def draw(self, surface):

        if self.selected:
            surface.blit(self.selected_image, (0, self._y_pix))

        elif self.hovered:
            surface.blit(self.hovered_image, (0, self._y_pix))

        else:
            surface.blit(self._image, (0, self._y_pix))

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 35)
            text = font.render(self.text, 1, (77, 77, 77))
            surface.blit(text, (
                self._x_pix + (self._width / 2 - text.get_width() / 2 + 2),
                self._y_pix + (self._height / 2 - text.get_height() / 2) - 5))


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
            return {"unit": (CELL_SIZE * x_ + (CELL_SIZE - UNIT_SIZE) / 2,
                             CELL_SIZE * y_ + (CELL_SIZE - UNIT_SIZE) / 2),
                    "cell": (x_ * CELL_SIZE, y_ * CELL_SIZE),
                    "action": (x_ * CELL_SIZE, y_ * CELL_SIZE)}

        bordered_y = None
        bordered_x = None
        bordered_type = None

        hovered_button = None
        selected_button = None

        while len(self.queue) > 0:

            command = self.queue[0]

            # log.mprint('got some commands: ' + str(command))

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

            if command[0] == "deselectAll":
                self.redraw_buttons = True
                bordered_type = None
                self.draw("frame")

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
            self.draw("frame")  # , "toolbar")
            frame = pygame.image.load(PICS[bordered_type]).convert_alpha()
            self.__frame_layer.blit(frame, positions_to_blit(bordered_x, bordered_y)[bordered_type])

        self.screen.blit(self.__field_layer, (0, 0))
        self.screen.blit(self.__units_layer, (0, 0))
        self.screen.blit(self.__buttons_layer, (CELL_SIZE * self.xCells, 0))
        self.screen.blit(self.__frame_layer, (0, 0))
        self.screen.blit(self.__toolbar_layer, (0, self.field_h))

        self.py_game.update_display()

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
        if "toolbar" in args:
            self.create_toolbar_layer()

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

    # отрисовка toolbar

    def create_toolbar_layer(self):
        if self.__toolbar_layer is None:
            self.__toolbar_layer = pygame.Surface((self.w, TOOLBAR_HEIGHT))

        score_pic = pygame.image.load(PICS["coins"]).convert_alpha()
        embl1 = pygame.image.load(PICS["emblem0"]).convert_alpha()
        embl2 = pygame.image.load(PICS["emblem1"]).convert_alpha()
        # для подстветки чувака который сейчас ходит
        color1 = RED
        color2 = COLOR
        if self.data.cur_step_name == 1:
            color1 = COLOR
            color2 = RED

        font = pygame.font.SysFont('comicsans', 70)

        name1 = font.render('Ivan            :{}              :{}'.format(
            self.data.score["Ivan"], self.data.num_units["Ivan"]), 1, color1)

        name2 = font.render('Egor            :{}             :{}'.format(
            self.data.score["Egor"], self.data.num_units["Egor"]), 1, color2)

        self.__toolbar_layer.fill((228, 213, 126))

        self.__toolbar_layer.blit(name1, (8, 13))
        self.__toolbar_layer.blit(score_pic, (CELL_SIZE, 0))
        self.__toolbar_layer.blit(embl1, (CELL_SIZE * 2 + 12, 8))

        self.__toolbar_layer.blit(name2, (CELL_SIZE * 3 + 10, 13))
        self.__toolbar_layer.blit(score_pic, (CELL_SIZE * 4, 0))
        self.__toolbar_layer.blit(embl2, (CELL_SIZE * 5 + 5, 6))

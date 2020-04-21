import pygame
import random

from game.display.Display import Display
from game.game_data import PyGame
from game.game_data.units.Units import Unit
from game.logs.Logs import Logs

# устанавливаем цвет логов
log = Logs("Yellow")

# размер одной ячейки(квадратной) в пикселях
CELL_SIZE = PyGame.CELL_SIZE
UNIT_SIZE = PyGame.UNIT_SIZE

PICS = {"mines": "pics/Mine.png", "barrack": "pics/Barrack.png",
        0: "pics/Valley.png", 1: "pics/Mountain.png", "archers": "pics/Archer.png",
        "warriors": "pics/Warrior.png", "miners": "pics/Miner.png", "unit": "pics/Frame_unit.png",
        "cell": "pics/Frame_cell.png", "action": "pics/Frame_cell.png" }

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
av_but_com = {0: "attack", 1: "move", 2: "create", 3: "build", 4: "upgrade"}


class PyGButtons(pygame.sprite.Sprite):
    def __init__(self):
        self.buttons = list()
        internal = pygame.image.load("pics/Button.png").convert_alpha()
        for i in range(5):
            self.buttons.append(
                Button(5 * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE, internal, av_but_com[i]))

    def render(self, dest):
        for i in range(self.buttons.__len__()):
            self.buttons[i].draw(dest, i)


class Button:
    def __init__(self, x, y, width, height, image, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = image

    def draw(self, surface, i):
        surface.blit(self.image, (CELL_SIZE * 5, CELL_SIZE * i))

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (77, 77, 77))
            surface.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2),
            self.y + (self.height / 2 - text.get_height() / 2)))

    def selected(self):
        pass


class PyGBuilding(pygame.sprite.Sprite):
    pass

class PyGameDisplay(Display):

    def __init__(self, py_game_, w, h, queue=None):
        super().__init__()
        self.data = None
        self.queue = queue
        self.py_game = py_game_
        # столбец для кнопок
        self.w = (w + 1) * CELL_SIZE
        self.h = (h + 1) * CELL_SIZE
        self.py_game.init_screen(self.w, self.h)
        self.screen = self.py_game.get_screen()

        self.__field_layer = None
        self.__units_layer = None
        self.__buttons_layer = None
        self.__frame_layer = None
        self.__buildings_layer = None

        self.pyg_cells = None
        self.pyg_units = None
        self.pyg_buttons = None
        self.pyg_buildings = None

        self.field_created = False

        log.print('PyGame Display created!')

    # как раз тут все данные из game_data, с которыми взаимодействует контроллер
    def set_data(self, data):
        self.data = data

    def get_screen(self):
        return self.py_game.get_screen()

    def update(self):
        if len(self.queue) > 0:
            log.print('got some commands: ' + str(self.queue))

            if self.queue[0][0] == "select":
                y = int(self.queue[0][1][0][0])
                x = int(self.queue[0][1][0][1])

                frame = pygame.image.load(PICS[self.queue[0][1][1]]).convert_alpha()
                self.__frame_layer = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
                if self.queue[0][1][1] == "unit":

                    self.__frame_layer.blit(frame, (
                        CELL_SIZE * x + (CELL_SIZE - UNIT_SIZE) / 2,
                        CELL_SIZE * y + (CELL_SIZE - UNIT_SIZE) / 2))
                else:
                    self.__frame_layer.blit(frame, (x * CELL_SIZE, y * CELL_SIZE))

            self.queue.popleft()

        if not self.field_created:
            self.field_created = True
            self.draw(all_=True)

        # self.screen.fill((255, 255, 255, 255))
        self.screen.blit(self.__field_layer, (0, 0))
        self.screen.blit(self.__units_layer, (0, 0))
        self.screen.blit(self.__buttons_layer, (0, 0))
        self.screen.blit(self.__frame_layer, (0, 0))

        self.py_game.update_display()
        # log.print('Display updated')

    def draw(self, all_=False, units=True):
        if all_:
            self.create_field_layer()
            self.create_units_layer()
            self.create_buttons_layer()
        if units:
            self.create_units_layer()

        self.__frame_layer = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)

    def create_units_layer(self):
        if self.data is None:
            raise Exception
        # создание слоя из юнитов
        self.pyg_units = PyGUnits(self.data.units)
        if self.__units_layer is None:
            self.__units_layer = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)

        self.__units_layer.fill(0)

        # их отрисовка
        self.pyg_units.render(self.__units_layer)

    def create_buttons_layer(self):
        # создание слоя из кнопок
        self.pyg_buttons = PyGButtons()
        if self.__buttons_layer is None:
            self.__buttons_layer = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)

        self.__buttons_layer.fill(0)

        # их отрисовка
        self.pyg_buttons.render(self.__buttons_layer)

    def create_field_layer(self):
        if self.data is None:
            raise Exception
        # создание слоя из cell
        self.pyg_cells = PyGCells(self.data._cells)
        self.__field_layer = pygame.Surface((self.w, self.h))
        # их отрисовка
        self.pyg_cells.render(self.__field_layer)

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


class PyGCells:

    def __init__(self, cells):
        n = 0

        self.cells = list()
        self.cell_id_on_coord = dict()

        for i in range(len(cells)):
            for j in range(len(cells[i])):
                # create PyGCell from cell[i][j] (class game_data.Cell) and append it to self.cells (class PyGCell)
                # меняем координаты местами. Так удобнее будет в pygame. Сначала позиция по горизонтали(ширине),
                # потом - по вертикали(высоте)
                pyg_cell = PyGCell(cells[i][j], n, j, i)
                self.cells.append(pyg_cell)
                # меняем координаты местами. Так удобнее будет в pygame. Сначала позиция по горизонтали(ширине),
                # потом - по вертикали(высоте)
                self.cell_id_on_coord[(j, i)] = n
                n += 1

    def create_coord_for_cell(self, x, y):
        return CELL_SIZE * x, CELL_SIZE * y

    def render(self, dest):
        for pyg_cell in self.cells:
            dest.blit(pyg_cell.surf, self.create_coord_for_cell(pyg_cell.x, pyg_cell.y))


i = 0


class PyGCell(pygame.sprite.Sprite):

    def __init__(self, cell, id__, x_, y_):
        self.id_ = id__
        self.x = x_
        self.y = y_
        super().__init__()
        self.surf = pygame.Surface((CELL_SIZE, CELL_SIZE))
        # internal = pygame.Surface((CELL_SIZE * 0.9, CELL_SIZE * 0.9))
        global i
        # internal.fill(((i + 100) % 255, i % 255, (i + 70) % 255))
        # пока что расставляем текстуры в шахматном порядке
        if cell._building == "mines":
            internal = pygame.image.load("pics/Mine.png").convert_alpha()
        elif cell._building == "barrack":
            internal = pygame.image.load("pics/Barrack.png").convert_alpha()
        else:
            if (self.x + self.y) % 2 == 0:
                internal = pygame.image.load("pics/Valley.png").convert_alpha()
            else:
                internal = pygame.image.load("pics/Mountain.png").convert_alpha()

        i += 20
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

        elif unit.type == "archers":
            internal = pygame.image.load("pics/Archer.png").convert_alpha()

        elif unit.type == "warriors":
            internal = pygame.image.load("pics/Warrior.png").convert_alpha()

        elif unit.type == "miners":
            internal = pygame.image.load("pics/Miner.png").convert_alpha()

        else:
            # черный фон никогда не должно выводиться
            internal = pygame.Surface((UNIT_SIZE, UNIT_SIZE))
            internal.fill((0, 0, 0))

        self.surf.blit(internal, (UNIT_SIZE * 0, UNIT_SIZE * 0))

        if unit.player != "died":
            f1 = pygame.font.Font(None, 18)
            text_level = f1.render('Lvl {}'.format(unit.get_level()), 1, (102, 51, 51))
            self.surf.blit(text_level, (UNIT_SIZE * 0.1, UNIT_SIZE * 0.74))

        # self.rect = self.surf.get_rect()


class PyGBuilding(pygame.sprite.Sprite):
    pass


class PyGameDisplay(Display):

    def __init__(self, py_game_, w, h, queue=None):
        super().__init__()
        self.data = None
        self.queue = queue
        self.py_game = py_game_
        self.w = w * CELL_SIZE
        self.h = h * CELL_SIZE
        self.py_game.init_screen(self.w, self.h)
        self.screen = self.py_game.get_screen()

        self.__field_layer = None
        self.__units_layer = None
        self.__frame_layer = None
        self.__buildings_layer = None

        self.pyg_cells = None
        self.pyg_units = None
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
                if self.queue[0][1][1] == "unit":
                    frame = pygame.image.load("pics/Frame_unit.png").convert_alpha()
                    y = int(self.queue[0][1][0][0])
                    x = int(self.queue[0][1][0][1])
                    self.__frame_layer = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
                    self.__frame_layer.blit(frame, (
                    CELL_SIZE * x + (CELL_SIZE - UNIT_SIZE) / 2, CELL_SIZE * y + (CELL_SIZE - UNIT_SIZE) / 2))
                else:
                    y = int(self.queue[0][1][0][0])
                    x = int(self.queue[0][1][0][1])
                    frame = pygame.image.load("pics/Frame_cell.png").convert_alpha()
                    self.__frame_layer = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
                    self.__frame_layer.blit(frame, (x * CELL_SIZE, y * CELL_SIZE))

            self.queue.popleft()

        if not self.field_created:
            self.field_created = True
            self.draw(all_=True)

        # self.screen.fill((255, 255, 255, 255))
        self.screen.blit(self.__field_layer, (0, 0))
        self.screen.blit(self.__units_layer, (0, 0))
        self.screen.blit(self.__frame_layer, (0, 0))

        self.py_game.update_display()
        # log.print('Display updated')

    def draw(self, all_=False, units=True):
        if all_:
            self.create_field_layer()
            self.create_units_layer()
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

    def create_field_layer(self):
        if self.data is None:
            raise Exception
        # создание слоя из cell
        self.pyg_cells = PyGCells(self.data._cells)
        self.__field_layer = pygame.Surface((self.w, self.h))
        # их отрисовка
        self.pyg_cells.render(self.__field_layer)

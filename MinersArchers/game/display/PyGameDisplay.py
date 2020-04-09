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
    cells = list()
    cell_id_on_coord = dict()

    def __init__(self, cells):
        n = 0
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
    id_ = 0
    x = None
    y = None
    is_select = False

    def __init__(self, cell, id__, x_, y_):
        self.id_ = id__
        self.x = x_
        self.y = y_
        super().__init__()
        self.surf = pygame.Surface((CELL_SIZE, CELL_SIZE))
        # internal = pygame.Surface((CELL_SIZE * 0.9, CELL_SIZE * 0.9))
        global i
        # internal.fill(((i + 100) % 255, i % 255, (i + 70) % 255))
        self.is_selected()
        # пока что расставляем текстуры в шахматном порядке
        if cell._building == "mines":
            internal = pygame.image.load("Mine.png").convert_alpha()
        elif cell._building == "barrack":
            internal = pygame.image.load("Barrack.png").convert_alpha()
        else:
            if (self.x + self.y) % 2 == 0:
                internal = pygame.image.load("Valley.png").convert_alpha()
            else:
                internal = pygame.image.load("Mountain.png").convert_alpha()

        i += 20
        self.surf.blit(internal, (CELL_SIZE * 0, CELL_SIZE * 0))
        self.rect = self.surf.get_rect()

    def is_selected(self):
        if self.is_select:
            external = pygame.image.load("Frame_cell.png").convert()
            self.surf.blit(external, (UNIT_SIZE * 0, UNIT_SIZE * 0))


class PyGUnits:
    units = list()
    units_id_on_coord = dict()

    def __init__(self, units):
        n = 0
        # перевод словаря из юнитов из game_data в двмумерный список
        for (i_, j_) in units.keys():
            unit = units[(i_, j_)]
            self.units.append(PyGUnit(unit, j_, i_, n))
            self.units_id_on_coord[(j_, i_)] = unit
            n += 1

    def create_coord_for_unit(self, x, y):
        return CELL_SIZE * x + (CELL_SIZE - UNIT_SIZE) / 2, CELL_SIZE * y + (CELL_SIZE - UNIT_SIZE) / 2

    def render(self, dest):
        for pyg_unit in self.units:
            dest.blit(pyg_unit.surf, self.create_coord_for_unit(pyg_unit.x, pyg_unit.y))


class PyGUnit(pygame.sprite.Sprite):
    id_ = 0
    x = None
    y = None
    is_select = False

    def __init__(self, unit, x_, y_, id__):
        self.id_ = id__
        self.x = x_
        self.y = y_
        super().__init__()
        self.surf = pygame.Surface((UNIT_SIZE, UNIT_SIZE), flags=pygame.SRCALPHA)

        # обработка мертвого юнита!!!вместо него будем выводить пока белый цвет->свободное место
        if unit.get_level() == 0:
            internal = pygame.Surface((UNIT_SIZE, UNIT_SIZE))
            internal.fill((255, 255, 255))
            # если убрать, будут видны старые слои
            # internal.set_colorkey((255, 255, 255))

        elif unit.type == "archers":
            internal = pygame.image.load("Archer.png").convert_alpha()

        elif unit.type == "warriors":
            internal = pygame.image.load("Warrior.png").convert_alpha()

        elif unit.type == "miners":
            internal = pygame.image.load("Miner.png").convert_alpha()

        else:
            # черный фон никогда не должно выводиться
            internal = pygame.Surface((UNIT_SIZE, UNIT_SIZE))
            internal.fill((0, 0, 0))

        self.surf.blit(internal, (UNIT_SIZE * 0, UNIT_SIZE * 0))

        if unit.player != "died":
            f1 = pygame.font.Font(None, 18)
            text_level = f1.render('Lvl {}'.format(unit.get_level()), 1, (102, 51, 51))
            self.surf.blit(text_level, (UNIT_SIZE * 0.1, UNIT_SIZE * 0.74))

        self.rect = self.surf.get_rect()

    def is_selected(self):
        if self.is_select:
            external = pygame.image.load("Frame_unit.png").convert_alpha()
            self.surf.blit(external, (UNIT_SIZE * 0, UNIT_SIZE * 0))


class PyGBuilding(pygame.sprite.Sprite):
    pass


class PyGameDisplay(Display):
    w = None
    h = None

    __field_layer = None
    __units_layer = None
    __frame_layer = None
    __buildings_layer = None
    __screen = None

    pyg_cells = None
    pyg_units = None
    pyg_buildings = None

    field_created = False

    def __init__(self, py_game_, w, h, queue=None):
        super().__init__()
        self.data = None
        self.queue = queue
        self.py_game = py_game_
        self.w = w * CELL_SIZE
        self.h = h * CELL_SIZE
        self.py_game.init_screen(self.w, self.h)
        self.screen = self.py_game.get_screen()
        log.print('PyGame Display created!')

    # как раз тут все данные из game_data, с которыми взаимодействует контроллер
    def set_data(self, data):
        self.data = data

    def get_screen(self):
        return self.py_game.get_screen()

    def update(self):

        if len(self.queue) > 0:
            log.print('got some commands: ' + str(*self.queue))
            # !!!
            if self.queue[0][0] == "select":
                if self.queue[0][1][1] == "unit":
                    frame = pygame.image.load("Frame_unit.png").convert_alpha()
                    y = int(self.queue[0][1][0][0])
                    x = int(self.queue[0][1][0][1])
                    self.__frame_layer = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
                    self.__frame_layer.blit(frame, (CELL_SIZE * x + (CELL_SIZE - UNIT_SIZE) / 2, CELL_SIZE * y + (CELL_SIZE - UNIT_SIZE) / 2))
                else:
                    y = int(self.queue[0][1][0][0])
                    x = int(self.queue[0][1][0][1])
                    frame = pygame.image.load("Frame_cell.png").convert_alpha()
                    self.__frame_layer = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
                    self.__frame_layer.blit(frame, (x * CELL_SIZE, y * CELL_SIZE))

            self.queue.popleft()

        if not self.field_created:
            self.draw()
            self.field_created = True

        self.screen.fill((255, 255, 255))
        self.screen.blit(self.__field_layer, (0, 0))
        self.screen.blit(self.__units_layer, (0, 0))
        self.screen.blit(self.__frame_layer, (0, 0))

        self.py_game.update_display()
        # log.print('Display updated')

    def draw(self):
        self.create_field_layer()
        self.create_units_layer()
        self.__frame_layer = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)

    def create_units_layer(self):
        if self.data is None:
            raise Exception
        # создание слоя из юнитов
        self.pyg_units = PyGUnits(self.data.units)
        self.__units_layer = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        # их отрисовка
        self.pyg_units.render(self.__units_layer)

    def create_field_layer(self):
        if self.data is None:
            raise Exception
        # создание слоя из cell
        self.pyg_cells = PyGCells(self.data._cells)
        self.__field_layer = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        # их отрисовка
        self.pyg_cells.render(self.__field_layer)

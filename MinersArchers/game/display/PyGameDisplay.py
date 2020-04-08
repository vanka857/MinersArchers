from game.display.Display import Display
from game.game_data.PyGame import PyGame
from game.game_data.units.Units import Unit
import pygame

# размер одной ячейки(квадратной) в пикселях
CELL_SIZE = 200
UNIT_SIZE = 100


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

    def __init__(self, cell, id__, x_, y_):
        self.id_ = id__
        self.x = x_
        self.y = y_
        super().__init__()
        self.surf = pygame.Surface((CELL_SIZE, CELL_SIZE))
        internal = pygame.Surface((CELL_SIZE * 0.9, CELL_SIZE * 0.9))
        global i
        internal.fill(((i + 100) % 255, i % 255, (i + 70) % 255))
        i += 20
        self.surf.blit(internal, (CELL_SIZE * 0.05, CELL_SIZE * 0.05))
        self.rect = self.surf.get_rect()


class PyGUnits:
    units = list()
    units_id_on_coord = dict()

    def __init__(self, units):
        n = 0
        for (i_, j_) in units.keys():
            unit = units[(i_, j_)]
            self.units.append(PyGUnit(unit, j_, i_, n))
            self.units_id_on_coord[(j_, i_)] =  unit
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

    def __init__(self, unit, x_, y_, id__):
        self.id_ = id__
        self.x = x_
        self.y = y_
        super().__init__()
        self.surf = pygame.Surface((UNIT_SIZE, UNIT_SIZE))
        internal = pygame.Surface((UNIT_SIZE * 0.9, UNIT_SIZE * 0.9))
        internal.fill((255, 255, 255))
        self.surf.blit(internal, (UNIT_SIZE * 0.05, UNIT_SIZE * 0.05))
        self.rect = self.surf.get_rect()


class PyGBuilding(pygame.sprite.Sprite):
    pass


class PyGameDisplay(Display):

    w = None
    h = None

    __field_layer = None
    __units_layer = None
    __buildings_layer = None
    __screen = None

    pyg_cells = None
    pyg_units = None
    pyg_buildings = None

    field_created = False

    def __init__(self, py_game_, w, h):
        super().__init__()
        self.data = None
        self.py_game = py_game_
        self.w = w * CELL_SIZE
        self.h = h * CELL_SIZE
        self.py_game.init_screen(self.w, self.h)
        self.screen = self.py_game.get_screen()
        print('PyGame Display created!')

    def set_data(self, data):
        self.data = data

    def get_screen(self):
        return self.py_game.get_screen()

    def update(self):
        if True:
            self.draw()
        self.py_game.update_display()
        print('Display updated')

    def draw(self):
        if not self.field_created:
            self.field_created = True
            self.create_field_layer()
            self.create_units_layer()

        self.screen.fill((255, 255, 255))
        self.screen.blit(self.__field_layer, (0, 0))
        self.screen.blit(self.__units_layer, (0, 0))

    def create_units_layer(self):
        if self.data is None:
            raise Exception
        self.pyg_units = PyGUnits(self.data.units)
        self.__units_layer = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        self.pyg_units.render(self.__units_layer)

    def create_field_layer(self):
        if self.data is None:
            raise Exception
        self.pyg_cells = PyGCells(self.data._cells)
        self.__field_layer = pygame.Surface((self.w, self.h))
        self.pyg_cells.render(self.__field_layer)

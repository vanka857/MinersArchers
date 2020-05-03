from game.game_data.cells.Cell_pygame import PyGCell
from game.game_data.units.Unit_pygame import PyGUnit
from game.pygame_.Group import Group


class PyGCells(Group):
    def __init__(self, cells):
        n = 0
        self.cells = list()

        for (i, j) in cells.keys():
            # TODO своп координат
            pyg_cell = PyGCell(n, cells[(i, j)], j, i)
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
            pyg_unit = PyGUnit(n, unit)

            self.units.append(pyg_unit)
            n += 1
        Group.__init__(self, self.units)

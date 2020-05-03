import pygame

from game.game_data.cells.Cell import Cell
from game.pygame_ import PyGame
from game.pygame_.Object import Object
from game.pygame_.PyGame import PICS

# размер одной ячейки(квадратной) в пикселях
CELL_SIZE = PyGame.CELL_SIZE


class PyGCell(Object, Cell):
    # TODO не передавать лишнее
    def __init__(self, id__, cell: Cell, x_: int, y_: int):
        Object.__init__(self, id__, *self.create_coordinates(x_, y_), CELL_SIZE, CELL_SIZE)

        image = pygame.image.load(PICS["cell2"])
        self.load_image(image)

        Cell.__init__(self, x=x_, y=y_, relief=cell._relief)

    def create_coordinates(self, x: int, y: int) -> (int, int):
        return CELL_SIZE * x, CELL_SIZE * y

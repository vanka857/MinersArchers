import pygame

from game.game_data.cells.PygCell import CELL_SIZE
from game.game_data.units.Unit import Unit
from game.pygame_ import PyGame
from game.pygame_.Object import Object
from game.pygame_.PyGame import PICS


class PyGUnit(Object, Unit):
    def __init__(self, id__, unit: Unit):
        # на этом моменте свапаем координаты
        # инициализация Object
        Object.__init__(self, id__, *self.create_coordinates(*reversed(unit.get_cords())), UNIT_SIZE, UNIT_SIZE)

        image = pygame.image.load(PICS[unit.type]).convert_alpha()
        self.load_image(image, pygame.SRCALPHA)

        # инициализация Unit
        Unit.__init__(self, unit.get_player(), unit.get_level(), unit.get_type(), *unit.get_cords())

    def draw(self, surface, pos=None):
        if self.get_level() != 0:
            f1 = pygame.font.SysFont('comicsans', 28)
            text_level = f1.render('lvl:{}'.format(self.get_level()), 1, (50, 50, 50))
            text_name = f1.render('{}'.format(self.player), 1, (50, 50, 50))

            self.draw_on_me(text_level, (UNIT_SIZE * 0.1 - 5, UNIT_SIZE * 0.8 - 7))
            self.draw_on_me(text_name, (UNIT_SIZE * 0.6 - 5, UNIT_SIZE * 0.8 - 7))
        else:
            # TODO этого по-хорошему не должно быть
            internal = pygame.Surface((UNIT_SIZE, UNIT_SIZE), flags=pygame.SRCALPHA)
            internal.fill(0)
            self.load_image(internal, flags=pygame.SRCALPHA)

        super().draw(surface, pos)

    def create_coordinates(self, x: int, y: int) -> (int, int):
        return CELL_SIZE * x + (CELL_SIZE - UNIT_SIZE) / 2, CELL_SIZE * y + (CELL_SIZE - UNIT_SIZE) / 2


UNIT_SIZE = PyGame.UNIT_SIZE

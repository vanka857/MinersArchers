# coding=utf-8

import pygame
import json

from game import pygame_
from game.display.Display import Display
from game.game_data.cells.Cell_pygame import CELL_SIZE
from game.game_data.field.Field_pygame import PyGCells, PyGUnits
from game.logs.Logs import Logs
from game.pygame_ import PICS_pygame, font_family
from game.pygame_.Group import Group
from game.pygame_.Object import Object
from static import resource_path, config_path

with open(config_path("field.json"), "r") as read_file:
    field = json.load(read_file)

TOOLBAR_HEIGHT = field["TOOLBAR_HEIGHT"]
COLOR = tuple(field["COLOR"])
RED = tuple(field["RED"])
CELL_SIZE = field["CELL_SIZE"]
UNIT_SIZE = field["UNIT_SIZE"]

# устанавливаем цвет логов
log = Logs("Yellow")

# кнопки
av_but_com = {0: "attack", 1: "move", 2: "create", 3: "upgrade"}


class PyGButtons(Group):
    def __init__(self):
        self.buttons = list()
        button = pygame.image.load(PICS_pygame["button"]).convert_alpha()
        button_h = pygame.image.load(PICS_pygame["buttonHovered"]).convert_alpha()
        button_s = pygame.image.load(PICS_pygame["buttonSelected"]).convert_alpha()

        for i in range(len(av_but_com)):
            self.buttons.append(
                Button(0, i * CELL_SIZE, CELL_SIZE, CELL_SIZE, button, button_h, button_s, av_but_com[i]))

        Group.__init__(self, self.buttons)


class Button(Object):
    def __init__(self, x, y, width, height, image, hovered_image, selected_image, text=''):
        Object.__init__(self, 0, x, y, width, height)
        self.load_image(image, pygame.SRCALPHA)

        self.text = text

        self.image = image
        self.hovered_image = hovered_image
        self.selected_image = selected_image
        self.selected = False
        self.hovered = False

    def draw(self, surface: pygame.Surface, pos=None):

        if self.selected:
            self.load_image(self.selected_image, pygame.SRCALPHA)
        elif self.hovered:
            self.load_image(self.hovered_image, pygame.SRCALPHA)
        else:
            self.load_image(self.image, pygame.SRCALPHA)

        if self.text != '':
            font = pygame.font.Font(font_family, 28)
            text = font.render(self.text, 1, (77, 77, 77))
            self.draw_on_me(text, ((self._width / 2 - text.get_width() / 2 + 2),
                                   (self._height / 2 - text.get_height() / 2) - 5))

        super().draw(surface, (0, self._y_pix))

class PyGameDisplay(Display):

    def __init__(self, w, h):
        super().__init__()
        self.data = None

        self.field_w = w * CELL_SIZE
        self.field_h = h * CELL_SIZE
        self.xCells = w
        self.yCells = h

        # столбец для кнопок
        self.w = (w + 1) * CELL_SIZE
        self.h = h * CELL_SIZE + TOOLBAR_HEIGHT
        self.screen = pygame_.init_screen(self.w, self.h)

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

    redraw_buttons = False

    def update(self):
        # определение координат, куда накладывать рамку
        def positions_to_blit(x_, y_):
            return {"unit": (CELL_SIZE * x_ + (CELL_SIZE - UNIT_SIZE) / 2,
                             CELL_SIZE * y_ + (CELL_SIZE - UNIT_SIZE) / 2),
                    "cell": (x_ * CELL_SIZE, y_ * CELL_SIZE),
                    "action": (x_ * CELL_SIZE, y_ * CELL_SIZE)}

        if not self.field_created:
            self.field_created = True
            self.draw("all")

        if self.data.hovered:
            # если мышка над кнопкой, нужно как-то выделить кнопку
            coord = self.data.hovered[0]
            y = coord[0]
            button = pygame.image.load(PICS_pygame["buttonHovered"]).convert_alpha()
            font = pygame.font.Font(font_family, 28)
            text = font.render(av_but_com[y], 1, (77, 77, 77))
            button.blit(text, ((CELL_SIZE / 2 - text.get_width() / 2 + 2),
                               (CELL_SIZE / 2 - text.get_height() / 2) - 5))

            self.__buttons_layer.blit(button, (0, CELL_SIZE * coord[0]))
        else:
            self.create_buttons_layer()

        if self.data.selected is None:
            self.__frame_layer = pygame.Surface((self.field_w, self.field_h), pygame.SRCALPHA, 32)
            self.__frame_layer.fill(0)

        else:
            selected = self.data.selected
            coord = selected[0]

            names = {"cell": "cell_frame", "unit": "unit_frame"}

            name = selected[1]
            if name in list(names.keys()):
                pic_name = {"cell": "cell_frame", "unit": "unit_frame"}[name]
                frame = pygame.image.load(PICS_pygame[pic_name]).convert_alpha()
                # своп координат происходит здесь
                # очищаем слой с рамками, накладываем новую рамку
                self.__frame_layer = pygame.Surface((self.field_w, self.field_h), pygame.SRCALPHA, 32)
                self.__frame_layer.blit(frame, positions_to_blit(coord[1], coord[0])[name])
            if name == "action" and self.data.hovered:
                # если кликнута кнопка
                # нужно вывести нажатую кнопку
                coord = self.data.selected[0]
                y = coord[0]
                button = pygame.image.load(PICS_pygame["buttonSelected"]).convert_alpha()
                font = pygame.font.Font(font_family, 28)
                text = font.render(av_but_com[y], 1, (77, 77, 77))
                button.blit(text, ((CELL_SIZE / 2 - text.get_width() / 2 + 2),
                                   (CELL_SIZE / 2 - text.get_height() / 2) - 5))

                self.__buttons_layer.blit(button, (0, CELL_SIZE * coord[0]))
                pass

        self.screen.blit(self.__field_layer, (0, 0))
        self.screen.blit(self.__units_layer, (0, 0))
        self.screen.blit(self.__buttons_layer, (CELL_SIZE * self.xCells, 0))
        self.screen.blit(self.__toolbar_layer, (0, self.field_h))
        self.screen.blit(self.__frame_layer, (0, 0))

        pygame_.update_display()

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

        # TODO сделать select and hover внутри pygame_.Object
        if self.data.selected is not None and self.data.selected[1] == "cell":
            log.mprint("smth")
            k = 0
            for (i, j) in self.data.keys:
                if (i, j) == self.data.selected[0]:
                    self.pyg_cells.objects[k].select(pygame.image.load(PICS_pygame["cell_frame"]).convert_alpha())
                k += 1

        self.__field_layer = pygame.Surface((self.field_w, self.field_h))
        # их отрисовка
        self.pyg_cells.render(self.__field_layer)

    # отрисовка toolbar
    def create_toolbar_layer(self):
        if self.__toolbar_layer is None:
            self.__toolbar_layer = pygame.Surface((self.w, TOOLBAR_HEIGHT))

        score_pic = pygame.image.load(PICS_pygame["coins"]).convert_alpha()
        emblem1 = pygame.image.load(PICS_pygame["emblem0"]).convert_alpha()
        emblem2 = pygame.image.load(PICS_pygame["emblem1"]).convert_alpha()
        # для подстветки чувака который сейчас ходит
        color1 = RED
        color2 = COLOR
        if self.data.cur_step_name == 1:
            color1 = COLOR
            color2 = RED

        font = pygame.font.Font(font_family, 45)

        names = list(self.data.players.keys())
        name_1 = names[0]
        name_2 = names[1]

        name1 = font.render('{}            :{}              :{}'.format(name_1, self.data.players[name_1].get_score(),
                                                                        self.data.players[name_1].get_num_units()), 1,
                            color1)

        name2 = font.render('{}            :{}             :{}'.format(name_2, self.data.players[name_2].get_score(),
                                                                       self.data.players[name_2].get_num_units()), 1,
                            color2)

        self.__toolbar_layer.fill((228, 213, 126))
        self.__toolbar_layer.fill((228, 213, 126))

        self.__toolbar_layer.blit(name2, (8, 13))
        self.__toolbar_layer.blit(score_pic, (CELL_SIZE, 0))
        self.__toolbar_layer.blit(emblem2, (CELL_SIZE * 2 + 12, 8))

        self.__toolbar_layer.blit(name1, (CELL_SIZE * 3 + 10, 13))
        self.__toolbar_layer.blit(score_pic, (CELL_SIZE * 4, 0))
        self.__toolbar_layer.blit(emblem1, (CELL_SIZE * 5 + 5, 6))

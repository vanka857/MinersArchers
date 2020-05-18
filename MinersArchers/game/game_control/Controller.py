import math
from collections import Iterable

import game.game_data.cells.Cell as cell
import game.game_data.units.Unit as unit
from game import pygame_
from game.logs.Logs import Logs
from .Command import Command
# устанавливаем цвет логов
from ..game_data.Data import Player

log = Logs("Green")


def all_elements(values):
    for value in values:
        if isinstance(value, Iterable):
            for elem in all_elements(value):
                yield elem
        else:
            yield value


class Controller:
    # __game_data = 0

    def __init__(self, inp_data):
        self.__game_data = inp_data
        self.keys = None
        self.command = Command()
        self.quit_func = None

    # последний элемент списка должен быть именем игрока
    def main_control(self, command: Command, name_of_player: str):

        log.mprint("main controller got command: " + str(command))

        # провера на то, что не залезаем за края
        h1 = int(command.coords[0][0])
        w1 = int(command.coords[0][1])

        # провера на то, что не залезаем за края
        if h1 >= self.__game_data.get_size_field()[0] or w1 >= self.__game_data.get_size_field()[1] \
                or h1 < 0 or w1 < 0:
            log.mprint("You are out of the field! Check coordinates!")
            return 1

        if name_of_player != self.__game_data.units[h1, w1].player and not \
                (self.__game_data.units[h1, w1].player == "died" and command.command == "create"):
            log.mprint("You can't do it! It is not your cell or union!")
            return 1

        else:
            f = getattr(Controller, command.command)
            # исполняем команду (функцию с соответствующим именем) по названию команды

            # !координаты передаем в распакованном виде
            return f(self, list(all_elements(command.coords)), name_of_player)

    def create(self, coords: list, name: str):
        # если баланс 0
        if self.__game_data.players[name].get_score() == 0:
            log.mprint("You have no coins to create a unit!")
            return 1

        # если на этой позиции уже кто-то есть
        if self.__game_data.units[int(coords[0]), int(coords[1])].get_level() > 0:
            log.mprint("You can upgrade your unit!")
            return 1
        else:
            # установим тип из command и левел 1
            unit_creator = unit.Creator()
            # !!!пока у разных игроков разные типы - следовательно
            self.__game_data.units[(int(coords[0]), int(coords[1]))] = \
                unit_creator.create_unit(name, self.__game_data.TIPS[name], int(coords[0]), int(coords[1]), 1)
            # и снимаем монету за создание юнита
            self.__game_data.players[name].down_score()
            return 0

    def attack(self, coords: list, name: str):
        # провекра на то, что мы не пытаемся залезть за края
        h1 = int(coords[0])
        w1 = int(coords[1])

        h2 = int(coords[2])
        w2 = int(coords[3])

        if h2 >= self.__game_data.get_size_field()[0] or w2 >= self.__game_data.get_size_field()[1] \
                or h2 < 0 or w2 < 0:
            log.mprint("You are out of the field! Check coordinates!")
            return 1

        # если пытаемся напасть на себя же
        if self.__game_data.units[(h2, w2)].player == name:
            log.mprint("You are trying to attack yourself!")
            return 1

        if self.__game_data.units[(h2, w2)].get_level == 0:
            # если на той позиции никого нет, просто переносим отряд
            self.move(coords, name)
        else:
            # иначе все сделано по правилам и можем нападать
            # пока считаем, что можем ходить только в 4 стороны
            if math.fabs(h1 - h2) + math.fabs(w1 - w2) > 1:
                log.mprint("You can go only up, down, left and right!")
                return 1
            # unit1 - нападает, unit2 - защищается

            unit1 = self.__game_data.units[(h1, w1)]
            unit2 = self.__game_data.units[(h2, w2)]
            level1 = unit1.get_level()
            level2 = unit2.get_level()

            if level1 > level2:
                unit1.set_level(level1 - level2)
                unit1.set_cords(h2, w2)
                self.__game_data.units[(h2, w2)] = unit1
                self.__game_data.units[(h1, w1)] = self.__game_data.units[(-1, -1)]
                # увеличиваем его очки
                for i in range(level2):
                    self.__game_data.players[name].up_score()
                # указываем на мертвого
                return 0
            elif level1 == level2:
                # когда совпадают уровни, просто уничтожаем обе армии
                self.__game_data.units[(h1, w1)] = self.__game_data.units[(-1, -1)]
                self.__game_data.units[(h2, w2)] = self.__game_data.units[(-1, -1)]
                # увеличиваем его очки
                for i in range(level2):
                    self.__game_data.players[name].up_score()
                return 0
            else:
                unit2.set_level(level2 - level1)
                self.__game_data.units[(h1, w1)] = self.__game_data.units[(-1, -1)]
                return 0

    def move(self, coords: list, name: str):
        h1 = int(coords[0])
        w1 = int(coords[1])
        h2 = int(coords[2])
        w2 = int(coords[3])

        if math.fabs(h1 - h2) + math.fabs(w1 - w2) > 1:
            log.mprint("You can go only up, down, left and right!")
            return 1

        if h2 >= self.__game_data.get_size_field()[0] or w2 >= self.__game_data.get_size_field()[1] \
                or h2 < 0 or w2 < 0:
            log.mprint("You are out of the field! Check coordinates!")
            return 1

        # если там уже кто-то есть
        if self.__game_data.units[(h2, w2)].get_level() > 0:
            log.mprint("You can only attack this unit!")
            return 1

        else:
            unit1 = self.__game_data.units[(h1, w1)]
            unit1.set_cords(h2, w2)
            self.__game_data.units[(h2, w2)] = unit1
            self.__game_data.units[(h1, w1)] = self.__game_data.units[(-1, -1)]

            return 0

    def upgrade(self, coords: list, name: str):
        h1 = int(coords[0])
        w1 = int(coords[1])

        if self.__game_data.players[name].get_score() == 0:
            log.mprint("You have no coins to upgrade the unit!")
            return 1
        # и снимаем монету за создание юнита
        self.__game_data.players[name].down_score()

        self.__game_data.units[(h1, w1)].set_level(self.__game_data.units[(h1, w1)].level + 1)

        return 0

    def build(self, coords: list, name: str):
        h1 = int(coords[0])
        w1 = int(coords[1])

        # если на этой позиции уже кто-то есть
        if self.__game_data.units[(h1, w1)].player != name:
            log.mprint("You can't build on different unit!")
            return 1
        else:
            # создаем либо бараки, либо шахты
            # пока что только шахты
            cell_creator = cell.Creator()
            self.__game_data._cells[h1][w1] = cell_creator.create_building("mines", name)
            return 0

    available_button_commands = {0: "attack", 1: "move", 2: "create", 3: "upgrade"}

    def mouse_click(self, x, y):
        # вызывается из dispatcher при нажатии мыши

        # получаем координаты игрового поля и тип объекта, который был выбран мышью
        selected_object = pygame_.get_object_on_coords(x, y)

        if selected_object is None:
            return

        self.__game_data.selected = selected_object

        # если ожидаем команду и получаем ее
        if selected_object[1] == "action":
            # получаем имя команды по нажатой кнопке
            command_str = self.available_button_commands[selected_object[0][0]]

            # устанавливаем команду
            self.command.set_command(command_str)

        # иначе если ждали не команду (а координаты)
        elif selected_object[1] in {"cell", "unit"}:

            # добавляем координаты к команде
            self.command.append_coords(selected_object[0])

    def mouse_move(self, x, y):
        # вызывается из dispatcher при движении мыши
        hovered_object = pygame_.get_object_on_coords(x, y)

        if hovered_object and hovered_object[1] == "action":
            self.__game_data.hovered = hovered_object
        else:
            self.__game_data.hovered = None

    def set_keys(self, keys: dict):
        # инициализация кнопок
        self.keys = keys

    def key_pressed(self, key):
        # если кнопка для нас не существует
        if key not in self.keys:
            return

        # если была нажата кнопка ESC
        if self.keys[key] == "escape":
            self.command.clear()
            self.__game_data.selected = None

        # если ожидаем команду и получаем ее
        elif self.keys[key] in ("create", "move", "attack", "upgrade"):

            # устанавливаем команду
            self.command.set_command(self.keys[key])




    def execute_command(self, player: Player):
        # если команда сформирована
        if self.command.finish():

            # выполняем записанную команду игроком Player
            result = self.main_control(self.command, player.get_name())
            self.command.clear()

            # возвращаем результат выполнения (0 - успешно, 1 - ошибка)
            return result

        return 1

    def set_quit_func(self, f):
        # устанавливаем функцию выхода из игры
        self.quit_func = f

    def quit(self):
        # Эта функция вызывается из dispatcher по нажатию на красный крестик
        self.quit_func()

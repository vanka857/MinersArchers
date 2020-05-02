import math

import game.game_data.cells.Cell as cell
import game.game_data.units.Units as unit
from game.logs.Logs import Logs

# устанавливаем цвет логов
log = Logs("Green")
TIPS = {"Egor": "warriors", "Ivan": "archers"}


class Controller:
    __game_data = 0

    def __init__(self, inp_data):
        self.__game_data = inp_data

    # последний элемент списка должен быть именем игрока
    def main_control(self, command, name_of_player):

        log.mprint("main controller got command:" + str(command))

        # провера на то, что не залезаем за края
        h1 = int(command[1])
        w1 = int(command[2])

        # провера на то, что не залезаем за края
        if h1 >= self.__game_data.get_size_field()[0] or w1 >= self.__game_data.get_size_field()[1] \
                or h1 < 0 or w1 < 0:
            log.mprint("You are out of the field! Check coordinates!")
            return 1

        if name_of_player != self.__game_data.units[h1, w1].player and not \
                (self.__game_data.units[h1, w1].player == "died" and command[0] == "create"):
            log.mprint("You can't do it! It is not your cell or union!")
            return 1

        else:
            f = getattr(Controller, command[0])
            # исполняем команду (функцию с соответствующим именем) по названию команды
            return f(self, command, name_of_player)

    def create(self, command, name):
        # если баланс 0
        if self.__game_data.score[name] == 0:
            log.mprint("You have no coins to create a unit!")
            return 1

        # если на этой позиции уже кто-то есть
        if self.__game_data.units[int(command[1]), int(command[2])].get_level() > 0:
            log.mprint("You can upgrade your unit!")
            return 1
        else:
            # установим тип из command и левел 1
            unit_creator = unit.Creator()
            # !!!пока у разных игроков разные типы - следовательно
            self.__game_data.units[(int(command[1]), int(command[2]))] = \
                unit_creator.create_unit(name, TIPS[name], int(command[1]), int(command[2]), 1)
            # и снимаем монету за создание юнита
            self.__game_data.down_score(name)
            return 0

    def attack(self, command, name):
        # провекра на то, что мы не пытаемся залезть за края
        h1 = int(command[1])
        w1 = int(command[2])

        h2 = int(command[3])
        w2 = int(command[4])

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
            self.move(command)
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
                    self.__game_data.up_score(name)
                # указываем на мертвого
                return 0
            elif level1 == level2:
                # когда совпадают уровни, просто уничтожаем обе армии
                self.__game_data.units[(h1, w1)] = self.__game_data.units[(-1, -1)]
                self.__game_data.units[(h2, w2)] = self.__game_data.units[(-1, -1)]
                # увеличиваем его очки
                for i in range(level2):
                    self.__game_data.up_score(name)
                return 0
            else:
                unit2.set_level(level2 - level1)
                self.__game_data.units[(h1, w1)] = self.__game_data.units[(-1, -1)]
                return 0

    def move(self, command, name):
        h1 = int(command[1])
        w1 = int(command[2])
        h2 = int(command[3])
        w2 = int(command[4])

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

    def upgrade(self, command, name):
        h1 = int(command[1])
        w1 = int(command[2])

        if self.__game_data.score[name] == 0:
            log.mprint("You have no coins to upgrade the unit!")
            return 1
        # и снимаем монету за создание юнита
        self.__game_data.down_score(name)

        self.__game_data.units[(h1, w1)].set_level(self.__game_data.units[(h1, w1)].level + 1)

        return 0

    def build(self, command, name):
        h1 = int(command[1])
        w1 = int(command[2])

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

import game.game_data.units.Units as unit
import math


class Controller:
    __game_data = 0

    def __init__(self, inp_data):
        self.__game_data = inp_data

    # последний элемент кортежа должен быть именем игрока
    def main_control(self, command, name_of_player):
        # провера на то, что не залезаем за края
        h1 = int(command[1])
        w1 = int(command[2])

        if h1 >= self.__game_data.get_size_field()[0] or w1 >= self.__game_data.get_size_field()[1]  \
                or h1 < 0 or w1 < 0:
            print("You are out of the field! Check coordinates!")
            return 1

        if name_of_player != self.__game_data.units[h1, w1].player and self.__game_data.units[h1, w1].player != "died":
            print("You can't do it! It is not your cell or union!")
            return 1

        else:
            if command[0] == "create":
                return self.create(command, name_of_player)

            elif command[0] == "attack":
                return self.attack(command, name_of_player)

            elif command[0] == "move":
                return self.move(command)

            elif command[0] == "upgrade":
                return self.upgrade(command)

            else:
                pass

    def create(self, command, name):
        # если на этой позиции уже кто-то есть
        if self.__game_data.units[int(command[1]), int(command[2])].level > 0:
            print("You can update your unit!")
            return 1
        else:
            # установим тип из command и левел 1
            unit_creator = unit.Creator()
            self.__game_data.units[(int(command[1]), int(command[2]))] = unit_creator.create_unit(name, command[3], 1)

    def attack(self, command, name):
        # провекра на то, что мы не пытаемся залезть за края
        h1 = int(command[1])
        w1 = int(command[2])

        h2 = int(command[3])
        w2 = int(command[4])

        if h2 >= self.__game_data.get_size_field()[0] or w2 >= self.__game_data.get_size_field()[1] \
                or h2 < 0 or w2 < 0:
            print("You are out of the field! Check coordinates!")
            return 1

        #если пытаемся напасть на себя же
        if self.__game_data.units[(h2, w2)].player == name:
            print("You are trying to attack yourself!")
            return 1

        if self.__game_data.units[(h2, w2)].get_level == 0:
            # если на той позиции никого нет, просто переносим отряд
            self.move(command, name)
        else:
            # иначе все сделано по правилам и можем нападать
            # пока считаем, что можем ходить только в 4 стороны
            if math.fabs(h1 - h2) + math.fabs(w1 - w2) > 1:
                print("You can go only up, down, left and right!")
                return 1
            # unit1 - нападает, unit2 - защищается

            unit1 = self.__game_data.units[(h1, w1)]
            unit2 = self.__game_data.units[(h2, w2)]
            level1 = unit1.get_level()
            level2 = unit2.get_level()

            if level1 >= level2:
                unit1.set_level(level1 - level2)
                self.__game_data.units[(h2, w2)] = unit1
                self.__game_data.units[(h1, w1)] = self.__game_data.units[(-1, -1)]
                # указываем на мертвого
            else:
                unit2.set_level(level2 - level1)
                self.__game_data.units[(h1, w1)] = self.__game_data.units[(-1, -1)]

    def move(self, command):
        h1 = int(command[1])
        w1 = int(command[2])
        h2 = int(command[3])
        w2 = int(command[4])

        # дома не двигаем
        if self.__game_data.units[(h2, w2)].type == "miners":
            print("You can't move miners!")
            return 1

        if math.fabs(h1 - h2) + math.fabs(w1 - w2) > 1:
            print("You can go only up, down, left and right!")
            return 1

        if h2 >= self.__game_data.get_size_field[0] or w2 >= self.__game_data.get_size_field[1] \
                or h2 < 0 or w2 < 0:
            print("You are out of the field! Check coordinates!")
            return 1

        # если там уже кто-то есть
        if self.__game_data.units[(h2, w2)].get_level() > 0:
            print("You can only attack this unit!")
            return 1

        else:
            unit1 = self.__game_data.units[(h1, w1)]
            self.__game_data.units[(h2, w2)] = unit1
            self.__game_data.units[(h1, w1)] = self.__game_data.units[(-1, -1)]

    def upgrade(self, command):
        h1 = int(command[1])
        w1 = int(command[2])

        self.__game_data.units[(h1, w1)].set_level(self.__game_data.units[(h1, w1)].level + 1)

import game.game_data.cells.Cell as cell
import game.game_data.units.Unit as unit
import json


class Data:
    __width = 0
    __height = 0
    units = None
    _cells = None

    def __init__(self, w, h):
        self.__width = w
        self.__height = h

        # будем хранить юнитов в словаре, ключ - пара координат
        self.units = dict()
        self._cells = dict()

        with open("game/players.json", "r") as read_file:
            json_players = json.load(read_file)

        name_1 = json_players["PLAYER_1"]["name"]
        score_1 = json_players["PLAYER_1"]["score"]
        name_2 = json_players["PLAYER_2"]["name"]
        score_2 = json_players["PLAYER_2"]["score"]
        # счет
        self.players = {name_1: Player(name_1, score_1), name_2: Player(name_2, score_2)}

        names = list(self.players.keys())
        # вот место, где устаналивается, у кого, какой игрок
        self.TIPS = {names[0]: "warriors", names[1]: "archers"}

        # показывает, чей сейчас ход
        self.cur_step_name = False

        # сделаем мертвого юнита, на которого будем ссылаться при удалении
        # у него особый игрок died и уровень - 0
        unit_creator = unit.Creator()
        self.units[(-1, -1)] = unit_creator.create_unit("died", "warriors", -1, -1, 0)

        # нормальная расстановка
        for i in range(h):
            self.units[i, (i + 1) % 2] = unit_creator.create_unit(names[1], self.TIPS[names[1]], i, (i + 1) % 2, 3)
            self.units[i, self.__width - 1 - i % 2] = unit_creator.create_unit(names[0], self.TIPS[names[0]], i,
                                                                               self.__width - 1 - i % 2, 3)
        for i in range(h):
            for j in range(w):
                if not (i, j) in self.units.keys():
                    self.units[(i, j)] = unit_creator.create_unit("died", "warriors", i, j, 0)

        for i in range(h):
            for j in range(w):
                self._cells[(i, j)] = cell.Cell(i, j)

    # возвращает размеры поля
    def get_size_field(self):
        return self.__height, self.__width

    def up_score(self, name):
        self.players[name].up_score()

    def down_score(self, name):
        self.players[name].down_score()


class Player:
    __name = ""
    __score = 0
    __num_units = 0

    # по дефолту начальный счет - 3
    def __init__(self, name, balance):
        self.__name = name
        self.__score = balance
        self.__num_units = 0

    def set_num_units(self, num):
        self.__num_units = num

    def get_num_units(self):
        return self.__num_units

    def get_score(self):
        return self.__score

    def up_score(self):
        self.__score += 1

    def down_score(self):
        self.__score -= 1

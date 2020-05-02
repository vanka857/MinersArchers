from abc import ABC, abstractmethod


class Cell:
    _relief = 0
    _building = "none"
    _inp_player = "none"

    def __init__(self, y, x, relief=0):
        self._relief = relief
        self._y = y
        self._x = x

    def get_coords(self):
        return self._y, self._x

    def set_player(self, inp_player):
        self._inp_player = inp_player

    def get_player(self):
        result = self._inp_player
        return result

    def build(self, building_type, inp_level, inp_player):
        #check
        self._building = UCI.create_building(building_type, inp_level, inp_player)


'''
class Relief(ABC):
    __relief_type = "none"
    #__relief_level = 0
    __amount_of_natural_resources = 1
    __habitability = 1
'''


class Building(ABC):
    def __init__(self, inp_player, inp_level=0):
        self.player = inp_player
        self.level = inp_level


class Barrack(Building):
    def __init__(self, inp_player):
        super().__init__(inp_player)
        self._building = "barrack"


class Mines(Building):
    def __init__(self, inp_player):
        super().__init__(inp_player)
        self._building = "mines"


class UCI(ABC):
    # параметризованный фабричный метод `create_unit`
    @abstractmethod
    def create_building(self, building_type, inp_player):
        raise NotImplementedError()


class Creator(UCI):
    def create_building(self, building_type, inp_player):
        if building_type == "barrack":
            return Barrack(inp_player)

        if building_type == "mines":
            return Mines(inp_player)

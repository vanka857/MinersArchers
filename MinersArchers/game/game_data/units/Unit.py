from abc import ABC, abstractmethod


# interface of Unit
class Unit(ABC):
    def __init__(self, inp_player, inp_level, inp_type, y, x):
        self.player = inp_player
        self.level = inp_level
        self.type = inp_type
        self._y = y
        self._x = x

    def action(self, **kwargs):
        pass
        # raise NotImplementedError()

    def set_level(self, lvl):
        self.level = lvl

    def get_level(self):
        return self.level

    def get_cords(self):
        return self._y, self._x

    def get_player(self):
        return self.player

    def set_cords(self, y, x):
        self._y = y
        self._x = x

    def get_type(self):
        return self.type

    # drawing
    def render(self):
        pass
        # raise NotImplementedError()

    # declaration for player
    def say(self):
        pass
        # raise NotImplementedError()


# concrete units
class Warrior(Unit):
    def action(self, enemy):
        pass

    def render(self):
        return "Wa{} ".format(self.level)

    def say(self):
        print("We are {} {} of {}!".format(self.level * 10, self.type, self.player))


class Archer(Unit):
    def action(self, enemy):
        pass

    def render(self):
        return "Ar{} ".format(self.level)

    def say(self):
        print("We are {} {} of {}!".format(self.level * 10, self.type, self.player))


class Miner(Unit):
    def action(self):
        pass
        # collect_money(self, hex)

    def render(self):
        return "Mi{} ".format(self.level)

    def say(self):
        print("We are {} {} of {}!".format(self.level * 10, self.type, self.player))


# UnitCreatorInterface
class UCI(ABC):
    # параметризованный фабричный метод `create_unit`
    @abstractmethod
    def create_unit(self, inp_type, inp_player, inp_level):
        raise NotImplementedError()


# это паттерн фабрика, пишется так для читаемости
class Creator(UCI):
    def create_unit(self, inp_player, inp_type, y, x, inp_level=0):
        if inp_type == "warriors":
            return Warrior(inp_player, inp_level, "warriors", y, x)

        if inp_type == "archers":
            return Archer(inp_player, inp_level, "archers", y, x)

        if inp_type == "miners":
            return Miner(inp_player, inp_level, "miners", y, x)

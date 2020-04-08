from abc import ABC, abstractmethod


# interface of Unit
class Unit(ABC):
    def __init__(self, inp_player, inp_level):
        self.player = inp_player
        self.level = inp_level
        self.type = "none"

    @abstractmethod
    def action(self, **kwargs):
        raise NotImplementedError()

    def set_level(self, lvl):
        self.level = lvl

    def get_level(self):
        return self.level

    # drawing
    def render(self):
        raise NotImplementedError()

    # declaration for player
    def say(self):
        raise NotImplementedError()


# concrete units
class Warrior(Unit):
    type = "warriors"

    def action(self, enemy):
        pass
        # attack

    def render(self):
        return "Wa{} ".format(self.level)

    def say(self):
        print("We are {} {} of {}!".format(self.level * 10, self.type, self.player))


class Archer(Unit):
    type = "archers"

    def action(self, enemy):
        pass
        # attack

    def render(self):
        return "Ar{} ".format(self.level)

    def say(self):
        print("We are {} {} of {}!".format(self.level * 10, self.type, self.player))


class Miner(Unit):
    type = "miners"

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


class Creator(UCI):
    def create_unit(self, inp_player, inp_type, inp_level=0):
        if inp_type == "warriors":
            return Warrior(inp_player, inp_level)

        if inp_type == "archers":
            return Archer(inp_player, inp_level)

        if inp_type == "miners":
            return Miner(inp_player, inp_level)

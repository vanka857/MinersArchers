from abc import ABC, abstractmethod


# interface of Unit
class Unit(ABC):
    def __init__(self, inp_player, inp_level=0):
        self.player = inp_player
        self.level = inp_level

    @abstractmethod
    def action(self):
        raise NotImplementedError()

    def set_level(self, lvl):
        self.level = lvl

    # drawing
    def render(self):
        raise NotImplementedError()

    # declaration for player
    def say(self):
        raise NotImplementedError()


# наивная реализация столкновения двух армий(кто меньше, то проигрывает)
def units_fight(unit1, unit2):
    assert unit1.player != unit2.player
    if unit2.level <= unit1.level:
        unit1.level -= unit2.level
        unit2.level = 0
        return True
    else:
        unit2.level -= unit1.level
        unit1.level = 0
        return False


# concrete units
class Warrior(Unit):
    type = "warriors"

    def action(self, enemy):
        if units_fight(self, enemy):
            print("We have won!")
        else:
            print("We have lost!")

    def render(self):
        return "Wa{} ".format(self.level)

    def say(self):
        print("We are {} {} of {}!".format(self.level * 10, self.type, self.player))


class Archer(Unit):
    type = "archers"

    def action(self, enemy):
        if units_fight(self, enemy):
            print("We have won!")
        else:
            print("We have lost!")

    def render(self):
        return "Ar{} ".format(self.level)

    def say(self):
        print("We are {} {} of {}!".format(self.level * 10, self.type, self.player))

# def collect_money(hex, unit):
#     print("Player {} has got {} coins!".format(unit.player, hex.relief / 10 * unit.level))


class Miner(Unit):
    type = "miners"

    def action(self):
        pass
        # collect_money(self, hex)

    def render(self):
        return "Wo{} ".format(self.level)

    def say(self):
        print("We are {} {} of {}!".format(self.level * 10, self.type, self.player))


# UnitCreatorInterface
class UCI(ABC):
    # параметризованный фабричный метод `create_unit`
    @abstractmethod
    def create_unit(self, inp_type, inp_player):
        raise NotImplementedError()


class Creator(UCI):
    def create_unit(self, inp_type, inp_player):
        if inp_type == "warriors":
            return Warrior(inp_player)

        if inp_type == "archers":
            return Archer(inp_player)

        if inp_type == "miners":
            return Miner(inp_player)


# как взаимодействовать с units
# from game.game_data import units
#
# app = units.CreateUnit()
#

# war1 = Creator.create_unit('warriors', 'vanya')
# war2 = Creator.create_unit('archers', 'egor')

#
# war1.action(war2)
#
# war1.say()
# war2.say()

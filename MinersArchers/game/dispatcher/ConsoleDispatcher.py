from game.dispatcher.Dispatcher import Dispatcher

COMMANDS = {"create": 0, "move": 0, "attack": 0, "upgrade": 0, "build": 0, "quit": 0}


class ConsoleDispatcher(Dispatcher):

    def __init__(self):
        super().__init__()
        # print("Console Dispatcher is ready!")

    def get_command(self):
        print("your turn! Please input command (", end='')
        # вывод доступных команд
        print(*COMMANDS, end=')\n')
        command = input()

        # пока не была введена доступная команда
        while command not in COMMANDS:
            print("your turn! Please input command (", end='')
            # вывод доступных команд
            print(*COMMANDS, end=')\n')
            command = input()
        return command

    def get_coords(self, number):
        print("Input {} coordinates in line:".format(number))
        coords = list(input().split())

        while len(coords) != number:
            print("Input {} coordinates in line:".format(number))
            coords = list(input().split())

        return coords

    def get_creation(self, x):
        print("What are you going to create on ({}, {})?(archers or warriors)".format(x[0], x[1]))
        creation = input()

        while creation != "archers" and creation != "miners" and creation != "warriors":
            print("What are you going to create on ({}, {})?".format(x[0], x[1]))
            creation = input()

        return creation

    def check_new_commands(self):
        return True, (self.step(),)

    def attack(self):
        print("from (..,..) and the (..,..)")
        attack_ = self.get_coords(4)
        print("You are going to attack from ({}, {}) the ({}, {})".format(attack_[0], attack_[1], attack_[2], attack_[3]))
        return "attack", attack_[0], attack_[1], attack_[2], attack_[3]

    def create(self):
        x = self.get_coords(2)
        creation = self.get_creation(x)

        return "create", x[0], x[1], creation

    def move(self):
        print("from (..,..) and to (..,..)")
        move_ = self.get_coords(4)
        print("You are going to move from ({}, {}) to ({}, {})".format(move_[0], move_[1], move_[2], move_[3]))
        return "move", move_[0], move_[1], move_[2], move_[3]

    def upgrade(self):
        x = self.get_coords(2)
        print("You are going to upgrade ({}, {})".format(x[0], x[1]))
        return "upgrade", x[0], x[1]

    def build(self):
        build_ = self.get_coords(2)
        print("You are build nothing at ({}, {}) cause it is not work now".format(build_[0], build_[1]))
        return "build", build_[0], build_[1]

    def quit(self):
        return "quit"

    # основной ход
    def step(self):
        command = self.get_command()

        # вызов команды по её имени из пространства имён модуля(класса) ConsoleDispatcher
        f = getattr(ConsoleDispatcher, command)
        return f(self)

from game.dispatcher.Dispatcher import Dispatcher


class ConsoleDispatcher(Dispatcher):
    def __init__(self):
        super().__init__()
        print("Console Dispatcher created!")

    def get_command(self):
        print("Your turn! Please input command(build, upgrade, move or attack)")
        command = input()

        while command != "build" and command != "move" and command != "attack" and command != "upgrade":
            print("Your turn! Please input command(build, upgrade, move or attack)")
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
        print("What are you going to build on ({}, {})?(archers, miners, warriors)".format(x[0], x[1]))
        creation = input()

        while creation != "archers" and creation != "miners" and creation != "warriors":
            print("What are you going to build on ({}, {})?".format(x[0], x[1]))
            creation = input()

        return creation

    # основной ход
    def step(self):
        command = self.get_command()

        if command == "build":
            x = self.get_coords(2)
            creation = self.get_creation(x)

            return "build", x[0], x[1], creation

        elif command == "attack":
            print("from (..,..) and to (..,..)")
            attack = self.get_coords(4)
            print("You are going to attack the ({}, {}) from ({}, {})".format(attack[0], attack[1], attack[2], attack[3]))
            return "attack", attack[0], attack[1], attack[2], attack[3]

        elif command == "move":
            print("from (..,..) and to (..,..)")
            move = self.get_coords(4)
            print("You are going to attack the ({}, {}) to ({}, {})".format(move[0], move[1], move[2], move[3]))
            return "move", move[0], move[1], move[2], move[3]

        elif command == "upgrade":
            x = self.get_coords(2)
            print("You are going to upgrade ({}, {})".format(x[0], x[1]))
            return "upgrade", x[0], x[1]

        else:
            print("There is no such command!")
            return 1

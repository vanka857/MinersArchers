from game.display.Display import Display


class ConsoleDisplay(Display):
    def __init__(self, sizes):
        self.weight = sizes[0]
        self.height = sizes[1]
        # создается пустой массив w * h элементов

        print("Console Display created!")
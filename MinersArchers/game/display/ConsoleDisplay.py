from game.display.Display import Display


class ConsoleDisplay(Display):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # создается пустой массив w * h элементов
        print("Console Display {} * {} created!".format(self.width, self.height))

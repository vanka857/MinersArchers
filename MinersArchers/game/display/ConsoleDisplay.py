from game.display.Display import Display


class ConsoleDisplay(Display):
    def __init__(self):
        super().__init__()
        print("Console Display created!")

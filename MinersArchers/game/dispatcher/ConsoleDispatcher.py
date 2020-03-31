from game.dispatcher.Dispatcher import Dispatcher


class ConsoleDispatcher(Dispatcher):
    def __init__(self):
        super().__init__()
        print("Console Dispatcher created!")

from game.display.ConsoleDisplay import ConsoleDisplay
from game.dispatcher.ConsoleDispatcher import ConsoleDispatcher
from game.game_data.Data import Data


class Game:
    __game_data = 0
    __event_dispatcher = 0
    __display = 0

    def __init__(self):
        self.__display = ConsoleDisplay()
        self.__event_dispatcher = ConsoleDispatcher()
        self.__game_data = Data()

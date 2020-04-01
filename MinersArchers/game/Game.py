from game.display.ConsoleDisplay import ConsoleDisplay
from game.dispatcher.ConsoleDispatcher import ConsoleDispatcher
from game.game_data.Data import Data


class Game:
    __game_data = 0
    __event_dispatcher = 0
    __display = 0

    def __init__(self):
        # пока что реализуем консольный вывод и консольный ввод
        #self.__display = ConsoleDisplay()
        self.__event_dispatcher = ConsoleDispatcher()
        self.__game_data = Data()

    # возвращает кортеж, на первом месте первая буква команды, далее координаты
    def get_console_command(self):
        res = self.__event_dispatcher.step()

        while res == 1:
            res = self.__event_dispatcher.step()

        return res

    # начало игры
    def start(self):
        print("Game has started!")
        command = self.get_console_command()
        print(command)

    def draw(self):
        # получаем размеры поля
        sizes = self.__game_data.size_field()
        self.__display(sizes)


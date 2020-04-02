from game.display.ConsoleDisplay import ConsoleDisplay
from game.dispatcher.ConsoleDispatcher import ConsoleDispatcher
from game.game_data.Data import Data


class Game:
    __game_data = 0
    __event_dispatcher = 0
    __display = 0
    __running = True

    def __init__(self, w=5, h=5):
        # пока что реализуем консольный вывод и консольный ввод
        self.__display = ConsoleDisplay(w, h)
        self.__event_dispatcher = ConsoleDispatcher()
        self.__game_data = Data(w, h)
        self.__display.data = self.__game_data.create_data_to_display()

    def __do_action(self, command):
        if command[0] == "quit":
                self.__running = False

    # начало игры
    def start(self):
        print("Game has started!")

        self.__display.set_data(self.__game_data.create_data_to_display())
        self.__display.update()

        while self.__running:
            has_new_commands, commands = self.__event_dispatcher.check_new_commands()
            # если есть новые команды
            if has_new_commands:
                for command in commands:
                    self.__do_action(command)
                    print(command)

                self.__display.set_data(self.__game_data.create_data_to_display())
                self.__display.update()

    def draw(self):
        # получаем размеры поля
        sizes = self.__game_data.get_size_field()
        #self.__display(*sizes)


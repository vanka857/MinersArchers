from game.display.ConsoleDisplay import ConsoleDisplay
from game.dispatcher.ConsoleDispatcher import ConsoleDispatcher
from game.game_data.Data import Data
from game.GameControl.Controller import Controller


class Game:
    __game_control = 0
    __game_data = 0
    __event_dispatcher = 0
    __display = 0
    __running = True

    def __init__(self, w=5, h=5):
        # console output
        self.__display = ConsoleDisplay(w, h)
        self.__event_dispatcher = ConsoleDispatcher()
        self.__game_data = Data(w, h)
        # у контроллера есть все данные об игре
        self.__game_control = Controller(self.__game_data)

    def __do_action(self, command, name):
        if command[0] == "quit":
            self.__running = False
        else:
            self.__game_control.main_control(command, name)

    # начало игры
    def start(self):
        print("Game has started!")

        self.__display.set_data(self.__game_data)
        # просто передача ссылки
        self.__display.update()

        count_steps = 0
        # игроки ходят по очереди 0 и 1
        while self.__running:
            count_steps = 1 - count_steps
            has_new_commands, commands = self.__event_dispatcher.check_new_commands()
            # если есть новые команды
            if has_new_commands:
                for command in commands:
                    self.__do_action(command, count_steps * "egor" + (1 - count_steps) * "ivan")

                self.__display.update()

    def draw(self):
        # получаем размеры поля
        sizes = self.__game_data.get_size_field()
        # self.__display(*sizes)

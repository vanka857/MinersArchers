# coding=utf-8
from game.display.ConsoleDisplay import ConsoleDisplay
from game.dispatcher.ConsoleDispatcher import ConsoleDispatcher
from game.game_data.Data import Data
from game.game_control.Controller import Controller
from game.game_data.PyGame import PyGame
from game.display.PyGameDisplay import PyGameDisplay
from game.dispatcher.PyGameDispatcher import PyGameDispatcher
import time


class Game:
    __game_control = 0
    __game_data = 0
    __event_dispatcher = 0
    __display = 0
    __running = True

    # игроки
    __players = ["ivan", "egor"]
    # id игрока
    __current_player = 0

    FRAME_TIME = 50

    def __init__(self, mode="console", w=5, h=5):
        self.__mode = mode
        if mode == "py_game":
            self.__py_game = PyGame()
            self.__display = PyGameDisplay(self.__py_game, w, h)
            self.__event_dispatcher = PyGameDispatcher(self.__py_game)
        elif mode == "console":
            # console output
            self.__display = ConsoleDisplay(w, h)
            self.__event_dispatcher = ConsoleDispatcher()
        else:
            print("Incorrect init!")
            raise Exception

        self.__game_data = Data(w, h)
        # у контроллера есть все данные об игре
        self.__game_control = Controller(self.__game_data)

    def __do_action(self, command, name):
        if command == "quit":
            # завершение программы
            self.__running = False
        else:
            # передача управления в контроллер
            self.__game_control.main_control(command, name)

    def __change_player(self):
        # игроки делают ходу по кругу
        self.__current_player = (self.__current_player + 1) % len(self.__players)

    def __get_player(self, id_):
        return self.__players[id_]

    # начало игры
    def start(self):
        print("Game has started!")

        self.__display.set_data(self.__game_data)
        # просто передача ссылки
        self.__display.update()

        last_frame_time = time.time()

        while self.__running:
            # Для вывода имени игрока, который ходит в данный момент
            # print(self.__get_player(self.__current_player), end=', ')
            has_new_commands, commands = self.__event_dispatcher.check_new_commands()
            # если есть новые команды
            if has_new_commands:
                for command in commands:
                    # передаем текущего игрока по его id
                    self.__do_action(command, self.__get_player(self.__current_player))

                    # ЕГОР, вот здесь нао сделать проверку, завершен ли ход
                    if "ход завершен":
                        # когда ход игрока закончен, меняем текущего игрока
                        self.__change_player()

            current_time = time.time()
            if (current_time - last_frame_time) * 1000 > self.FRAME_TIME:
                last_frame_time = current_time
                self.__display.update()

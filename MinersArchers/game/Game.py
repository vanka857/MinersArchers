# coding=utf-8

import time
from collections import deque

from game.dispatcher.ConsoleDispatcher import ConsoleDispatcher
from game.dispatcher.PyGameDispatcher import PyGameDispatcher
from game.display.ConsoleDisplay import ConsoleDisplay
from game.display.PyGameDisplay import PyGameDisplay
from game.game_control.Controller import Controller
from game.game_data.Data import Data
from game.logs.Logs import Logs
from game.pygame_.PyGame import PyGame

# устанавливаем цвет логов
log = Logs()


class Game:
    __game_control = 0
    __game_data = 0
    __event_dispatcher = 0
    __display = 0
    __running = True

    # игроки
    __players = ["Ivan", "Egor"]
    # баланс игроков
    __score = {__players[0]: 0, __players[1]: 0}
    # id игрока
    __current_player = 0

    FRAME_TIME = 100

    def __init__(self, w=5, h=5, mode="console"):
        self.__mode = mode
        if mode == "py_game":
            # создаем очередь сообщения для прямой отправки от
            # PyGameDispatcher в PyGameDisplay команд типа "select"
            self.pyg_message_queue = deque()

            # создаем god-object для работы с pygame_
            self.__py_game = PyGame()

            self.__display = PyGameDisplay(self.__py_game, w, h, self.pyg_message_queue)
            self.__event_dispatcher = PyGameDispatcher(self.__py_game, self.pyg_message_queue)

        elif mode == "console":
            # console output
            self.__display = ConsoleDisplay(w, h)
            self.__event_dispatcher = ConsoleDispatcher()

        else:
            log.mprint("Incorrect init!")
            raise Exception

        self.__game_data = Data(w, h)
        # у контроллера есть все данные об игре
        # у контроллера есть все данные об игре
        self.__game_control = Controller(self.__game_data)

    def if_end(self):
        # подсчет сколько у кого юнитов
        num1 = 0
        num2 = 0
        for para in self.__game_data.units.items():
            if para[1].player == "Egor":
                num1 += 1
            if para[1].player == "Ivan":
                num2 += 1

        self.__game_data.num_units["Egor"] = num1
        self.__game_data.num_units["Ivan"] = num2

        # проверка на то, что в обоих игроков есть юниты
        for para in self.__game_data.units.items():
            if para[1].player == "Egor":
                break
        else:
            log.mprint("Ivan win!!! End of the game")
            self.__running = 0

        for para in self.__game_data.units.items():
            if para[1].player == "Ivan":
                break
        else:
            log.mprint("Egor win!!! End of the game")
            self.__running = 0

    def __do_action(self, command, name):
        if command == "quit":
            # завершение программы
            self.__running = False
            return 0
        else:
            # передача управления в контроллер
            return self.__game_control.main_control(command, name)

    def __change_player(self):
        # игроки делают ходы по очереди
        self.__current_player = (self.__current_player + 1) % len(self.__players)

    def __get_player(self, id_):
        return self.__players[id_]

    # начало игры
    def start(self):
        log.mprint("-------------------------------------------------------------------")
        log.mprint("Game has started!")

        # пока что Draw видит все поле
        self.__display.set_data(self.__game_data)
        # TODO здесь не должно стоять if_end()! но сейчас без этого количество воинов не отображается при старте
        self.if_end()
        self.__display.update()

        last_frame_time = time.time()

        while self.__running:
            self.if_end()

            has_new_commands, commands = self.__event_dispatcher.check_new_commands()
            # если есть новые команды
            if has_new_commands:
                for command in commands:
                    # если контроллер вернул 0, все хорошо, меняем игрока,
                    # иначе цикл повторяется с тем же игроком
                    if self.__do_action(command, self.__get_player(self.__current_player)) == 0:
                        self.__game_data.cur_step_name = not self.__game_data.cur_step_name
                        # перерисовка поля
                        self.__display.draw("units", "toolbar")

                        # когда ход игрока закончен, меняем текущего игрока
                        self.__change_player()
                        log.mprint("player changed to:" + self.__get_player(self.__current_player))

            # для вызова self.__display.update() не чаще, чем каждые self.FRAME_TIME миллисекунд
            current_time = time.time()
            if (current_time - last_frame_time) * 1000 > self.FRAME_TIME:
                last_frame_time = current_time
                self.__display.update()
            else:
                time.sleep(0.1)

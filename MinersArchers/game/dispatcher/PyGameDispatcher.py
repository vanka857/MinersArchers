from collections.abc import Iterable

import pygame
# первые буквы команд для взаимодействия с юнитами через клавиартуру
from pygame.locals import (
    K_a,
    K_c,
    K_b,
    K_m,
    K_u,
    K_SPACE,
    K_ESCAPE
)

from game.game_data import PyGame
from game.logs.Logs import Logs
from .Command import Command
from .Dispatcher import Dispatcher

# устанавливаем цвет логов
log = Logs("Cyan")


def all_elements(values):
    for value in values:
        if isinstance(value, Iterable):
            for elem in all_elements(value):
                yield elem
        else:
            yield value


class PyGameDispatcher(Dispatcher):

    def __init__(self, py_game_, queue):
        super().__init__()
        self.py_game = py_game_
        self.command = Command()
        self.queue = queue

        log.mprint('PyGame Dispatcher created!')

    available_key_commands = {K_c: "create", K_a: "attack", K_b: "build", K_m: "move", K_u: "upgrade"}
    available_button_commands = {0: "attack", 1: "move", 2: "create", 3: "upgrade"}

    def check_new_commands(self) -> 'has_new_commands, commands':
        result = list()
        has_new_commands = False
        mouse_x = -1
        mouse_y = -1
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # log.mprint("____________'quit' command")
                result.append("quit")
                has_new_commands = True

            # пока что оставим поддержку ввода команд с клавиатуры
            if event.type == pygame.KEYDOWN:
                # log.mprint("____________keydown")

                # если ждем ввода команды and если нажата допустимая клавиша
                if self.command.status == "command" and event.key in self.available_key_commands:
                    #log.mprint("key command got")

                    # получаем имя команды по нажатой кнопке
                    command = self.available_key_commands[event.key]

                    # устанавливаем команду
                    self.command.set_command(command)

                if event.key == K_SPACE and self.command.status == "maked":
                    #log.mprint("key command sent")

                    # отправить команду (к результату работы всей функции check_new_commands())
                    # это жопный код, не разбирайся
                    has_new_commands = True
                    all_coords = list(all_elements(self.command.coords))
                    result.append((self.command.command, *all_coords))

                    # когда отправили команду, её можно сбросить
                    self.command.clear()

                if event.key == K_ESCAPE:
                    log.mprint("key command delete")
                    # удалить команду
                    self.command.clear()

            if event.type == pygame.MOUSEMOTION:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]

            selected_object = self.py_game.get_object_on_coords(mouse_x, mouse_y)
            if selected_object is not None and selected_object[1] == "action":
                self.queue.append(("hover", selected_object))

            if event.type == pygame.MOUSEBUTTONDOWN:
                # log.mprint("____________mouse button pressed: " + str(event.button))
                if event.button == 1 or event.button == 3:

                    # получаем координаты игрового поля и тип объекта, который был выбран мышью
                    selected_object = self.py_game.get_object_on_coords(event.pos[0], event.pos[1])

                    if selected_object is None:
                        continue

                    log.mprint("selecting: " + str(selected_object))
                    # добавляем координаты к команде

                    # отправить команду о выделении (она придет в PyGameDisplay)
                    self.queue.append(("select", selected_object))

                    # если ожидаем команду и получаем ее
                    if self.command.status == "command" and selected_object[1] == "action":
                        # получаем имя команды по нажатой кнопке
                        command = self.available_button_commands[selected_object[0][0]]

                        # устанавливаем команду
                        self.command.set_command(command)
                    else:

                        # если ожидается ввод ккординат
                        if self.command.status == "coords":

                            # добавляем координаты к команде
                            self.command.append_coords(selected_object[0])

        return has_new_commands, result

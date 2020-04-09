import pygame
from collections.abc import Iterable

from game.game_data import PyGame
from .Dispatcher import Dispatcher
from .Command import Command

from pygame.locals import (
    K_UP,
    K_a,
    K_c,
    K_b,
    K_m,
    K_u,
    K_SPACE,
    K_ESCAPE
)

from game.logs.Logs import Logs

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

        log.print('PyGame Dispatcher created!')

    available_key_commands = {K_c: "create", K_a: "attack", K_b: "build", K_m: "move", K_u: "upgrade"}

    def check_new_commands(self) -> 'has_new_commands, commands':
        result = list()
        has_new_commands = False
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # log.print_("____________'quit' command")
                result.append(("quit"))
                has_new_commands = True

            if event.type == pygame.KEYDOWN:
                # log.print_("____________keydown")

                # если ждем ввода команды and если нажата допустимая клавиша
                if self.command.status == "command" and event.key in self.available_key_commands:
                    log.print("key command got")

                    # получаем имя команды по нажатой кнопке
                    command = self.available_key_commands[event.key]

                    # устанавливаем команду
                    self.command.set_command(command)

                if event.key == K_SPACE and self.command.status == "maked":
                    log.print("key command sent")

                    # отправить команду (к результату работы всей функции check_new_commands())
                    # это жопный код, не разбирайся
                    has_new_commands = True
                    all_coords = list(all_elements(self.command.coords))
                    result.append((self.command.command, *all_coords))

                    # когда отправили команду, её можно сбросить
                    self.command.clear()

                if event.key == K_ESCAPE:
                    log.print("key command delete")
                    # удалить команду
                    self.command.clear()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # log.print_("____________mouse button pressed: " + str(event.button))
                if event.button == 1 or event.button == 3:
                    # получаем координаты игрового поля и тип объекта, который был выбран мышью
                    selected_object = PyGame.get_object_on_coords(event.pos[0], event.pos[1])

                    log.print("selecting: " + str(selected_object))
                    # добавляем координаты к команде

                    # отправить команду о выделении (она придет в PyGameDisplay)
                    self.queue.append(("select", selected_object))

                    # если ожидается ввод ккординат
                    if self.command.status == "coords":

                        # добавляем координаты к команде
                        self.command.append_coords(selected_object[0])

        return has_new_commands, result

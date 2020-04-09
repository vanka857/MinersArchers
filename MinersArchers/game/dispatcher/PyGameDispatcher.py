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
    n_of_args = {"create": 1, "move": 2, "attack": 2, "upgrade": 1, "build": 1}

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
                # если ждем ввода команды
                if self.command.status == "command" and event.key in self.available_key_commands:
                    log.print("key command got")
                    # то вводим команду
                    command = self.available_key_commands[event.key]
                    self.command.set_command(command)
                    # если нам нужно две координаты
                    if self.n_of_args[command] == 2:
                        # то ждем вторую координату
                        self.command.wait("coords")
                    else:
                        # если получили вторую координаты, то завершаем создание команды
                        self.command.status = "maked"

                if event.key == K_SPACE and self.command.status == "maked":
                    log.print("key command sent")
                    # отправить команду
                    has_new_commands = True
                    all_coords = list(all_elements(self.command.coords))
                    result.append((self.command.command, *all_coords))
                    self.command.clear()

                if event.key == K_ESCAPE:
                    log.print("key command delete")
                    # удалить команду
                    self.command.clear()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # log.print_("____________mouse button pressed: " + str(event.button))
                if event.button == 1 or event.button == 3:
                    # если нет текущей команды
                    if self.command.status == "coords":
                        # вставляем текущие координаты
                        selected_object = PyGame.get_object_on_coords(event.pos[0], event.pos[1])
                        log.print("selecting: " + str(selected_object))
                        self.command.append_coords(selected_object[0])
                        self.command.wait("command")

                        self.queue.append(("select", selected_object))
                        has_new_commands = True

        return has_new_commands, result

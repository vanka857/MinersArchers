import pygame
# первые буквы команд для взаимодействия с юнитами через клавиартуру
from pygame.locals import (
    K_ESCAPE
)

from game.game_control.Controller import Controller
from game.logs.Logs import Logs
from .Dispatcher import Dispatcher

# устанавливаем цвет логов
log = Logs("Cyan")


class PyGameDispatcher(Dispatcher):

    def __init__(self, controller: Controller):
        super().__init__()
        self.mouse_x = -1
        self.mouse_y = -1

        self.controller = controller

        log.mprint('PyGame Dispatcher created!')

    # available_key_commands = {K_c: "create", K_a: "attack", K_b: "build", K_m: "move", K_u: "upgrade"}

    def check_new_commands(self):
        self.controller.set_keys({"escape": K_ESCAPE})

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.controller.quit()

            # пока что оставим поддержку ввода команд с клавиатуры
            if event.type == pygame.KEYDOWN:

                if event.key == K_ESCAPE:
                    # оповещаем контроллер
                    self.controller.key_pressed(K_ESCAPE)

            if event.type == pygame.MOUSEMOTION:
                # оповещаем контроллер
                self.controller.mouse_move(event.pos[0], event.pos[1])

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3:
                    # оповещаем контроллер
                    self.controller.mouse_click(event.pos[0], event.pos[1])

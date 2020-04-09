import pygame


# класс, где реализован ввод + ввывод + обработка некоторых команд на pygame
class PyGame:

    def __init__(self):
        pygame.init()
        # просто создаем переменную
        self.__screen = None
        print("PyGame initialized")

    def init_screen(self, w, h):
        self.__screen = pygame.display.set_mode((w, h))

    def get_screen(self):
        return self.__screen

    def update_display(self):
        # Flip the display
        pygame.display.flip()

    def check_new_commands(self) -> 'has_new_commands, commands':
        # нуждается в доработке. сейчас передает все команды наверх, а должен часть из них обрабатывать самостоятельно
        result = list()
        has_new_commands = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                result.append("quit")
                has_new_commands = True
            if event.type == pygame.KEYDOWN:
                print("-----")
        return has_new_commands, result

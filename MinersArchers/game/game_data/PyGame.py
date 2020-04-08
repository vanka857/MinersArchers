import pygame

# класс, где реализован ввод + ввывод + обработка некоторых команд на pygame
class PyGame:
    # размер одной ячейки(квадратной) в пикселях
    CELL_SIZE = 100
    # хранит данные игрового поля
    field_data = None

    def __init__(self):
        pygame.init()
        # просто создаем переменную
        self.__screen = None
        print("PyGame initialized")

    def init_screen(self, w, h):
        self.__screen = pygame.display.set_mode([self.CELL_SIZE * w, self.CELL_SIZE * h])

    def get_screen(self):
        return self.__screen

    def set_field_data(self, data):
        self.field_data = data

    def draw(self):
        self.__screen.fill((255, 255, 255))

        # Draw a solid blue circle in the center
        pygame.draw.circle(self.__screen, (0, 0, 255), (250, 250), 75)

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

    def wait(self, time):
        # задержка, необходимая для
        pygame.time.wait(time)


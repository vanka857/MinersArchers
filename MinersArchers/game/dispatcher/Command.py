# Число аргументов команд
n_of_args = {"create": 1, "move": 2, "attack": 2, "upgrade": 1, "build": 1}


class Command:
    def __init__(self):
        # init - поле, показывающее, была ли "инициализирована" Command
        self.init = False
        # status - поле, показывающее, что в данный момент ожидает Command.
        # Любая Command изначально ожидает координаты
        self.status = "coords"
        self.command = None
        self.coords = list()

    def set_command(self, command):
        # если мы не ждали команду, то выходим
        if self.status != "command":
            return

        self.init = True
        self.command = command
        # пробуем сформировать команду
        self.finish()

    def append_coords(self, coords):
        # если мы не ждали координаты, то выходим
        if self.status != "coords":
            return

        self.init = True
        self.coords.append(coords)
        # пробуем сформировать Command
        self.finish()

    # попытка сформировать Command
    def finish(self):
        if self.command is None:
            # говорим, что ждем команду
            self.__wait("command")
        elif len(self.coords) != n_of_args[self.command]:
            # говорим, что ждем координаты
            self.__wait("coords")
        else:
            # отлично! формируем Command, т.е. говорим, что её статус = "maked"
            self.__wait("maked")

    def __wait(self, waiting):
        self.status = waiting

    # сбрасываем команду
    def clear(self):
        self.command = None
        self.coords.clear()
        self.init = False
        self.__wait("coords")

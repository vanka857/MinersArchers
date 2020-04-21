from game.display.Display import Display


class ConsoleDisplay(Display):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        # создается пустой массив w * h элементов
        print("Console Display {} * {} created!".format(self.width, self.height))

    def has_changes(self):
        return True

    def __cell_to_str(self, i, j):
        return "[({}, {}) b:{} u:{} pl:{}]".format(i, j, self._data._cells[i][j]._building,
                                                   self._data.units[(i, j)].render(),
                                                   self._data.units[(i, j)].player)

    def __draw(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.__cell_to_str(i, j), end=" ")
            print("\n")

    def update(self):
        if not self.has_changes():
            return

        self.__draw()
        super().update()

    def set_data(self, data):
        self._data = data

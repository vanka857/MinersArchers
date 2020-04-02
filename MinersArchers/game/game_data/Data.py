import game.game_data.units.Units as unit
import game.game_data.cells.Cell as cell


class Data:
    __width = 0
    __height = 0

    def __init__(self, w, h):
        self.__width = w
        self.__height = h
        self.__units_id = {}
        self.__cells = [[]]

        print('Creating game data:')

        unit_creator = unit.Creator()
        for i in range(w * h):
            self.__units_id[i] = unit_creator.create_unit("warriors", "vanya")
        for i in range(w * h):
            self.__units_id[i] = unit_creator.create_unit("warriors", "egor")

        for i in range(h):
            self.__cells.append([])
            for j in range(w):
                self.__cells[i].append([])
                self.__cells[i][j] = cell.Cell()

    # возвращает размеры поля
    def get_size_field(self):
        return {self.__width, self.__height}

    def create_data_to_display(self):
        return self.__cells


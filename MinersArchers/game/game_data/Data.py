import game.game_data.units.Units as unit
import game.game_data.cells.Cell as cell


class Data:
    __width = 0
    __height = 0

    def __init__(self, w, h):
        self.__width = w
        self.__height = h

        # будем хранить юнитов в словаре, ключ - пара координат
        self.units = dict()
        self._cells = [[]]
        # балланс игроков
        self.score_player_1 = 0
        self.score_player_2 = 0

        print('Creating game data:')

        # сделаем мертвого юнита, на которого будем ссылаться при удалении
        # у него особый игрок и уровень - 0
        unit_creator = unit.Creator()
        self.units[(-1, -1)] = unit_creator.create_unit("died", "warriors", 0)

        for i in range(h):
            for j in range(w):
                if (i + j) % 2 == 0:
                    self.units[(i, j)] = unit_creator.create_unit("egor", "warriors", i + j)
                else:
                    self.units[(i, j)] = unit_creator.create_unit("ivan", "warriors", i + j)

        for i in range(h):
            self._cells.append([])
            for j in range(w):
                self._cells[i].append([])
                self._cells[i][j] = cell.Cell()

    # возвращает размеры поля
    def get_size_field(self):
        return self.__height, self.__width

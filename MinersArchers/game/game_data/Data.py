import game.game_data.cells.Cell as cell
import game.game_data.units.Unit as unit


class Data:
    __width = 0
    __height = 0
    units = None
    _cells = None

    def __init__(self, w, h):
        self.__width = w
        self.__height = h

        # будем хранить юнитов в словаре, ключ - пара координат
        self.units = dict()
        self._cells = dict()

        # счет
        self.score = {"Egor": 3, "Ivan": 3}
        self.num_units = {"Egor": 0, "Ivan": 0}

        # показывает, чей сейчас ход
        self.cur_step_name = False

        # сделаем мертвого юнита, на которого будем ссылаться при удалении
        # у него особый игрок died и уровень - 0
        unit_creator = unit.Creator()
        self.units[(-1, -1)] = unit_creator.create_unit("died", "warriors", -1, -1, 0)

        # рандомная расстановка
        # for i in range(h):
        #     for j in range(w):
        #         ran = random.randint(0, 5)
        #         # пока что у всех уровень 3
        #         if ran == 4:
        #             self.units[(i, j)] = unit_creator.create_unit("died", "warriors", i, j, 0)
        #         elif ran % 2 == 0:
        #             self.units[(i, j)] = unit_creator.create_unit("Ivan", "archers", i, j, 3)
        #         else:
        #             self.units[(i, j)] = unit_creator.create_unit("Egor", "warriors", i, j, 3)

        # нормальная расстановка
        for i in range(h):
            self.units[i, (i + 1) % 2] = unit_creator.create_unit("Ivan", "archers", i, (i + 1) % 2, 3)
            self.units[i, self.__width - 1 - i % 2] = unit_creator.create_unit("Egor", "warriors", i,
                                                                               self.__width - 1 - i % 2, 3)
        for i in range(h):
            for j in range(w):
                if not (i, j) in self.units.keys():
                    self.units[(i, j)] = unit_creator.create_unit("died", "warriors", i, j, 0)

        for i in range(h):
            for j in range(w):
                self._cells[(i, j)] = cell.Cell(i, j)

    # возвращает размеры поля
    def get_size_field(self):
        return self.__height, self.__width

    def up_score(self, name):
        self.score[name] += 1

    def down_score(self, name):
        self.score[name] -= 1

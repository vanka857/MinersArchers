from game.game_data.field.Field import Field
import game.game_data.units.Units as u


class Data:
    def __init__(self, w, h):
        self.units_id = {}
        self.field = dict()

        print('Creating game data:')

        C = u.Creator()
        for i in range(w * h):
            self.units_id[i] = C.create_unit("warriors", "vanya")
        for i in range(w * h):
            self.units_id[i] = C.create_unit("warriors", "egor")

    # возвращает размеры поля
    def size_field(self):
        pass

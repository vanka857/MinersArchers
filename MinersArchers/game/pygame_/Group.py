import pygame


class Group(pygame.sprite.Group):

    def __init__(self, new_objects=()):
        super().__init__()
        self.objects = new_objects

    def add_object(self, new_object):
        self.objects.append(new_object)

    def update(self, differences):
        dif = self.get_dif()

    # на вход приходит массив старых хэшей
    def get_dif(self, old_hash=()):
        res = []
        for i in range(len(self.objects)):
            if self.objects[i].__hash__() != old_hash[i]:
                res.append(i)
        return res

    # отрисовка
    def render(self, dest):
        for obj in self.objects:
            obj.draw(dest)

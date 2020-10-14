import pygame


class Object(pygame.sprite.Sprite):
    def __init__(self, id_: int, x: int, y: int, width: int, height: int):
        # инициализация базового класса
        pygame.sprite.Sprite.__init__(self)
        # load image...
        self._id = id_
        # эти в пикселях
        self._y_pix = y
        self._x_pix = x

        self._height = height
        self._width = width
        self._image = None

        self.surf = None
        self.rect = None

    def get_coordinates(self):
        return self._x_pix, self._y_pix

    def get_size(self):
        return self._width, self._height

    # создание картинки
    def load_image(self, image: pygame.Surface, flags=0):
        self.surf = pygame.Surface((self._height, self._width), flags=flags)

        self.surf.blit(image, (0, 0))
        self.rect = self.surf.get_rect()

    def draw(self, surface, pos=None):
        # self.load_image()
        if not pos:
            pos = (self._x_pix, self._y_pix)

        surface.blit(self.surf, pos)

    def update(self, *args):
        """Hooked calling pygame_.sprite.Group.update() call"""
        pass

    def draw_on_me(self, surface: pygame.Surface, pos=None):
        if not pos:
            pos = (0, 0)

        self.surf.blit(surface, pos)
        self.rect = self.surf.get_rect()

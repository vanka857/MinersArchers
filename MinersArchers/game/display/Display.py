from abc import ABC, abstractmethod


class Display(ABC):
    _data = None

    @abstractmethod
    def __init__(self):
        # print('Creating Display: ')
        pass

    @abstractmethod
    def update(self):
        # print('Display updated')
        pass

    @abstractmethod
    def set_data(self, data):
        raise NotImplementedError()

    @abstractmethod
    def draw(self):
        pass

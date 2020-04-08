from abc import ABC, abstractmethod


class Display(ABC):

    _data = None

    @abstractmethod
    def __init__(self):
        print('Creating Display: ')

    @abstractmethod
    def update(self):
        print('Display updated')

    @abstractmethod
    def set_data(self, data):
        raise NotImplementedError()

    # для задержки основного цикла. На данный момент это костыль. Потом будет сделано через таймер между фреймами
    def wait(self, time=50):
        pass




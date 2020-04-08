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




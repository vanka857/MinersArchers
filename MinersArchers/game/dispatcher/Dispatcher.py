from abc import ABC, abstractmethod


class Dispatcher(ABC):
    @abstractmethod
    def __init__(self):
        print('Creating Dispatcher: ')

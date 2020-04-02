from abc import ABC, abstractmethod


class Dispatcher(ABC):
    @abstractmethod
    def __init__(self):
        print('Creating Dispatcher: ')

    @abstractmethod
    def check_new_commands(self) -> 'has_new_commands, commands':
        pass

from abc import ABC, abstractmethod


class Display(ABC):
    @abstractmethod
    def __init__(self):
        print('Creating Display: ')

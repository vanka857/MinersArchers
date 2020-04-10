import inspect

# Класс для вывода логов в консоль. Выводится в таком формате цветным текстом:
# [PYGAMEDISPATCHER.PY]: key command sent


class Color:
    # при выводе этих строк устанавливается цвет текста
    Red = '\033[91m'
    Green = '\033[92m'
    Yellow = '\033[93m'
    Blue = '\033[94m'
    Magenta = '\033[95m'
    Cyan = '\033[96m'
    White = '\033[97m'
    Grey = '\033[90m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Logs:

    def __init__(self, color_name="None"):
        self.color_name = color_name
        pass

    def print(self, *args, **kwargs):
        # Это для получения того места (файла), откуда была вызвана функция Log()::print
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)

        name = calframe[1][1]
        name = "[" + str(name).split('/')[-1].upper() + "]: "

        if self.color_name == "None":
            # цвет стандартный, ни на что не меняется
            color = ""
        else:
            # меняем цвет на установленный
            color = getattr(Color, self.color_name)

        # выводим имя файла нужным цветом, а затем сбрасываем цвет выводом Color.END
        print(color + name + Color.END, end='')
        # печатаем то, что надо было напечатать
        print(*args, **kwargs)

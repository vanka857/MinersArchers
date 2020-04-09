import inspect


class Color:

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
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)

        name = calframe[1][1]
        name = "[" + str(name).split('/')[-1].upper() + "]: "
        if self.color_name == "None":
            color = ""
        else:
            color = getattr(Color, self.color_name)

        print(color + name + Color.END, end='')
        print(*args, **kwargs)

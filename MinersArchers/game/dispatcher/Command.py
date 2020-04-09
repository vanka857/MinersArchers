class Command:
    def __init__(self):
        self.init = False
        self.status = "coords"
        self.command = None
        self.coords = list()

    def set_command(self, command):
        self.init = True
        self.command = command

    def append_coords(self, coords):
        self.init = True
        self.coords.append(coords)

    def wait(self, waiting):
        self.status = waiting

    def clear(self):
        self.command = None
        self.coords.clear()
        self.init = False
        self.wait("coords")

class Hello:
    def __init__(self, name):
        self.__name = name

    def msg(self):
        return F"Hello, {self.__name}!"

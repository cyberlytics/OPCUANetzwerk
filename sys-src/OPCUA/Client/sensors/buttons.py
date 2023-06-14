from sensors.button import Button

class Buttons(object):
    def __init__(self):
        self.__button1 = Button(16)
        self.__button2 = Button(25)
        self.__button3 = Button(23)
        self.__button4 = Button(18)

    @property
    def Button1(self):
        return self.__button1

    @property
    def Button2(self):
        return self.__button2

    @property
    def Button3(self):
        return self.__button3

    @property
    def Button4(self):
        return self.__button4





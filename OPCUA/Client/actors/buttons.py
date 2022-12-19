from actors.actor_base import ActorBase
from actors.button import Button

class Buttons(ActorBase):
    def __init__(self):
        self.__button1 = Button(16)
        self.__button2 = Button(25)
        self.__button3 = Button(23)
        self.__button4 = Button(18)







class EventHandler:
    def __init__(self):
        self.__cb = set()
    
    def subscribe(self, func):
        self.__cb.add(func)
        
    def unsubscribe(self, func):
        self.__cb.remove(func)
        
    def __call__(self, sender, args):
        for f in self.__cb:
            f(sender, args)





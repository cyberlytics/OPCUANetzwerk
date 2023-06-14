from helpers.event_handler import EventHandler

class OpcuaSubscriptionHandler(object):
    def __init__(self):
        self.__eh = EventHandler()

    def datachange_notification(self, node, val, data):
        self.__eh(self, {'node' : node , 'new' : val})

    def event_notification(self, event):
        print("Python: New event", event.EventType)

    @property
    def DataChanged(self):
        return self.__eh




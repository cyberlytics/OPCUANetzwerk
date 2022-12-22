import platform

class SystemInformation(object):
    def __init__(self):
        pass
    
    @property
    def hostname(self):
        return platform.node()
import platform, os
import netifaces as ni

class SystemInformation(object):
    def __init__(self):
        self.__cpu_dict = None
        self.__system_dict = None
    
    @property
    def Hostname(self):
        return platform.node()

    @property
    def IP(self):
        return ni.ifaddresses('tun0')[ni.AF_INET][0]['addr']

    @property
    def Vendor(self):
        return self.CPU_Dict['Vendor ID']

    @property
    def ModelName(self):
        return self.CPU_Dict['Model name']

    @property
    def NumberOfCpus(self):
        return self.CPU_Dict['Core(s) per socket']

    @property
    def Architecture(self):
        return self.CPU_Dict['Architecture']

    @property
    def ReleaseName(self):
        return self.System_Dict['VERSION_CODENAME']

    @property
    def Release(self):
        return self.System_Dict['VERSION_ID']

    @property
    def Distributor(self):
        return self.System_Dict['HOME_URL']

    @property
    def Version(self):
        return self.System_Dict['VERSION']

    @property
    def CPU_Dict(self):
        if self.__cpu_dict == None:
            self.__parse_lscpu()
        return self.__cpu_dict

    @property
    def System_Dict(self):
        if self.__system_dict == None:
            self.__parse_os_release()
        return self.__system_dict

    def __parse_os_release(self):
        var = os.popen('cat /etc/os-release').read().split('\n')
        var.remove(var[-1])
        self.__system_dict = {}
        for line in var:
            val = line.split('=')[1].replace('"', '')
            self.__system_dict[line.split('=')[0]] = val

    def __parse_lscpu(self):
        var = os.popen('lscpu').read().split('\n')
        var.remove(var[-1])
        self.__cpu_dict = {}
        for line in var:
            self.__cpu_dict[line.split(":")[0]] = line.split(":")[1].lstrip()
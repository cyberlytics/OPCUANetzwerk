from enum import Enum


from threading import Thread
import time
import os

class ConnectionHelper(object):
    def __init__(self, opcua_client):
        self.__opc = opcua_client

        self.OK = 0
        self.OPCUA_SERVER_NOT_REACHABLE = 1
        self.SERVER_NODE_NOT_REACHABLE = 2
        self.VPN_GATEWAY_NOT_REACHABLE = 3
        self.NO_INTERNET_CONNECTION = 4
        self.NOT_INITIALIZED = 5

        self.__status = self.NOT_INITIALIZED
        self.__connection_check_active = False
    
    @property
    def ConnectionCheckActive(self):
        return self.__connection_check_active

    @property
    def Status(self):
        return self.__status

    def start_connection_check(self):
        if self.__connection_check_active:
            return

        self.__connection_check_active = True
        self.__t = Thread(target=self.__connection_check, args=[])
        self.__t.start()
        
    def stop_connection_check(self):
        self.__connection_check_active = False

    def __connection_check(self):
        while self.ConnectionCheckActive:
            time.sleep(10)

            # OPCUA-Server reachable?
            if self.__opc.opcua_server_reachable():
                self.__status = self.OK
                continue
            self.__status = self.OPCUA_SERVER_NOT_REACHABLE

            # Server-Node reachable?
            if self.__server_reachable():
                continue
            self.__status = self.SERVER_NODE_NOT_REACHABLE

            # VPN-Gateway reachable?
            if self.__vpn_reachable():
                continue
            self.__status = self.VPN_GATEWAY_NOT_REACHABLE

            # Internet reachable?
            if self.__internet_reachable():
                continue
            self.__status = self.NO_INTERNET_CONNECTION

    def __server_reachable(self):
        return os.system('ping server.sn.local') == 0

    def __vpn_reachable(self):
        return os.system('ping ap1.home') == 0

    def __internet_reachable(self):
        return os.system('ping 8.8.8.8') == 0




from opcua import Server, ua
from time import sleep
    

if __name__ == "__main__":

    server = Server()
    server.set_endpoint("opc.tcp://127.0.0.1:4841")
    server.import_xml("Informationsmodell.xml")
    server.start()
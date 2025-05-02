import socket
import threading

class Server:
    def __init__(self, port):
        self.tuple = {}
        self.lock = threading.Lock()
        self.state = {
            "numtuples":0,
            "avertuple":0,
            "averkey":0,
            "avervalue":0, #string 
            "total_clients" :0,
            "total_operations":0, 
            "READs":0,
            "GETs":0, 
            "PUTs":0, 
            "errors":0
        }

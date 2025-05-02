import socket
import threading

class Server:
    def __init__(self, port):
        self.tuple = {}
        self.lock = threading.Lock()
        self.state = {
            "reads":0,
            "gets":0,
            "puts":0,
            "errs":0
        }
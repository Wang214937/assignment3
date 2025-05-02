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
        self.start_sever (port)

    def start_sever(self, port):
        host = 'localhost'
        port = port
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen()
        print("Server is running and ready to accept multiple client...")
        

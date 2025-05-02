import socket
import sys

class Client:
    def __init__(self, host, port,file_path):
        try:
            with open(file_path) as file:
                self.requests = [line.strip() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            sys.exit(1)

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
        except Exception as e:
            print(f"Error connecting to server: {e}")
        finally:
            client_socket.close()
            sys.exit(1)

    
    
    

       
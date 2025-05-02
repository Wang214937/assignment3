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


    

       
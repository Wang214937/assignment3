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

    def process_requests(self):
        for request in self.requests:
            parts = request.split(' ', 2)
            if len(parts) < 2:
                print(f"Invalid request format: {request}")
                continue
            command = parts[0]
            try:
                if command not in ["R", "G", "P"]:
                    print(f"Invalid command: {command}")
                    continue
                if command == "R":
                    self.handle_read(request[1:])
                elif command == "G":    
                    self.handle_get(request[1:])
                elif command == "P":
                    self.handle_put(request[1:])
            except Exception as e:
                print(f"Error processing request: {e}")
            finally:
                self.client_socket.close()
                sys.exit(1)     
    
    

       
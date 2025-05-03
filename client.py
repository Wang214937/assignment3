import socket
import sys

class Client:
    def __init__(self, host, port,file_path):
        self.host = host
        self.port = port
        self.file_path = file_path
        self.client_socket = None
        try:
            with open(file_path) as file:
                self.requests = [line.strip() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            sys.exit(1)

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            self.process_requests()
        except Exception as e:
            print(f"Error connecting to server: {e}")


    def process_requests(self):
        for request in self.requests:
            cmd_map = {
                "P": "PUT",
                "G": "GET",
                "R": "REMOVE"
            }
            parts = request.split().split(maxsplit=2)
            if not parts:
                continue
            cmd_str = parts[0]
            if cmd_str not in cmd_map:
                print(f"Unknown command: {cmd_str}")
                continue
            command = cmd_map[cmd_str]
            try:
                if command == "P":
                    if len(parts) != 3:
                        print(f"Invalid PUT request: {request}")
                        continue
                    key, value = parts[1], parts[2]
                    if len(key) > 999 or len(value) > 999:
                        print(f"Key or value too long: {key}, {value}")
                        continue
                    self.send_command(command, f"{key} {value}")
                elif command == "G" or command == "R":
                    self.send_command(command, parts[1])
                else:
                    print(f"Unknown command: {command}")
            except Exception as e:
                print(f"Error processing request: {e}")
    

    def send_command(self, command, value):
        try:
            message = f"{command}{value}"
            if len(message) > 999:
                print(f"Message too long: {message[:10]}")
                return
            header = f"{len(message):03d}".encode('utf-8')
            full_message = header + message.encode('utf-8')
            self.client_socket.send(full_message)

            response = self.client_socket.recv(3).decode('utf-8')
            if not response:
                print("No response from server")
                return
            response_len = int (response)
            response = self.client_socket.recv(response_len).decode('utf-8')
            print(f"{command} {value}:{response}")
        except Exception as e:
            print(f"Error sending command: {e}")
        finally:
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <host> <port> <file_path>")
        sys.exit(1)
    Client(sys.argv[1], int(sys.argv[2]), sys.argv[3])
        
            

       
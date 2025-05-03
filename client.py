import socket
import sys

class Client:
    def __init__(self, host, port,file_path):
        self.host = host
        self.port = port
        self.file_path = file_path
        self.sock = None
        try:
            with open(file_path) as file:
                self.requests = [line.strip() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            sys.exit(1)

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            self.process_requests()
        except Exception as e:
            print(f"Error connecting to server: {e}")
        finally:
            client_socket.close()


    def process_requests(self):
        for request in self.requests:
            parts = request.split(' ', 2)
            if len(parts) < 2:
                print(f"Invalid request format: {request}")
                continue
            command = parts[0]
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
            finally:
                self.client_socket.close()
                sys.exit(1)     
    

    def send_command(self, command, value):
        try:
            message = f"{command} {value}"
            if len(message) > 999:
                print(f"Message too long: {message}")
                return
            header = f"{len(message):03d}".encode('utf-8')
            full_message = header + message.encode('utf-8')
            self.sock.send(full_message)

            response = self.sock.recv(3).decode('utf-8')
            if not response:
                print("No response from server")
                return
            response_len = int (header.decode('utf-8'))
            response = self.sock.recv(response_len).decode('utf-8')
            print(f"{command} {value}:{response}")
        except Exception as e:
            print(f"Error sending command: {e}")
        finally:
            self.client_socket.close()
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <host> <port> <file_path>")
        sys.exit(1)
    Client(sys.argv[1], int(sys.argv[2]), sys.argv[3])
        
            

       
import socket
import threading
import time
import sys

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
        self.start_server (port)
        threading.Thread(target=self.print_stats, daemon=True).start()

    def start_server(self, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.listen()
        print("Server is running and ready to accept multiple client...")
        try:
            while True:
                client_socket, addr = server_socket.accept()
                self.state["total_clients"] += 1
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,addr))
                client_thread.start()
        except KeyboardInterrupt:
            print("Server is shutting down...")
        finally:
            server_socket.close()

    def handle_client(self,client_socket):
        try:
            while True:
                message = client_socket.recv(3).decode('utf-8')
                message_length = int(message)
                full_message = client_socket.recv(message_length).decode('utf-8')
                cmd, request = full_message[0], full_message[1:]
                print(f"client says: {message}")
                response = self.process_request(cmd, request)
                response_message = f"{len(response):03d}".encode('utf-8') + response.encode('utf-8')
                client_socket.send(response_message)
        except Exception as e:
            print(f"Error handling client: {e}" )
        finally:
            client_socket.close()
            print(f"Connection closed")
        
    def process_request(self, cmd, request):
        self.state["total_operations"] += 1
        response = ""
        try:
            if cmd == "R":
                self.state["READs"] += 1
                key = request
                with self.lock:
                    if key in self.tuple:
                        value = self.tuple(key)
                        response = f"READ {key} {value}"
                    else:
                        response = "Key not found"
                        self.state["errors"] += 1
            elif cmd == "G":
                self.state["GETs"] += 1
                key = request
                with self.lock:
                    if key in self.tuple:
                        value = self.tuple.pop[key]
                        self.state["numtuples"] -= 1
                        self.state["avertuple"] -= (len(key)+len(value))
                        self.state["averkey"] -= len(key)
                        self.state["avervalue"] -= len(value)
                        response = f"GET {key} {value},and deleted from the tuple"
                    else:
                        response = "Key not found"
                        self.state["errors"] += 1
            elif cmd == "P":
                self.state["PUTs"] += 1
                if ' ' not in request:
                    self.state["errors"] += 1
                    response = "Invalid PUT request"
                key, value = request.split(" ",1)
                with self.lock:
                    if key in self.tuple:
                        self.state["errors"] += 1
                        response = "Key already exists"
                    else:
                        self.tuple[key] = value
                        self.state["numtuples"] += 1
                        self.state["avertuple"] += len(key) + len(value)
                        self.state["averkey"] += len(key)
                        self.state["avervalue"] += len(value)
                        response = f"PUT {key} {value}"
            else:
                self.state["errors"] += 1
                response = "Invalid command"
        except Exception as e:
            self.state["errors"] += 1
            response = f"Error processing request: {e}"
        return response
        
                
    def print_stats(self):
        while True:
            time.sleep(10)
            print(f"Currrent tuples: {self.state['numtuples']}")
            if self.state["numtuples"] > 0:
                print(f"Average tuple size: {self.state['avertuple'] / self.state['numtuples']:.2f}")
                print(f"Average key size: {self.state['averkey'] / self.state['numtuples']:.2f}")
                print(f"Average value size: {self.state['avervalue'] / self.state['numtuples']:.2f}")
            print(f"Total clients: {self.state['total_clients']}")
            print(f"Total operations: {self.state['total_operations']}")
            print(f"READs: {self.state['READs']}")
            print(f"GETs: {self.state['GETs']}")
            print(f"PUTs: {self.state['PUTs']}")
            print(f"Errors: {self.state['errors']}")


    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    Server(int(sys.argv[1]))
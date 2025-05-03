import socket
import threading
import time
import sys

class Server:
    def __init__(self,port):
        self.tuple = {}
        self.lock = threading.Lock()
        self.state = {
            "numtuples":0,
            "avertuple":0,
            "averkey":0,
            "avervalue":0,      #string 
            "total_clients" :0,
            "total_operations":0, 
            "READs":0,
            "GETs":0, 
            "PUTs":0, 
            "errors":0
        }
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(5)
        print(f"Server listening on port {port}")
        threading.Thread(target=self.print_stats, daemon=True).start()
        self.start_server()

    def start_server(self):
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"New connection from {addr}")
                with self.lock:
                    self.state["total_clients"] += 1
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
        except KeyboardInterrupt:
            print("Server is shutting down...")
        finally:
            self.server_socket.close()

    def handle_client(self,client_socket):
        try:
            while True:
                header = client_socket.recv(3)
                if len(header) != 3:
                    break
                try:
                    message_length = int(header.decode('utf-8'))
                except ValueError:
                    break
                full_message = b''
                remaining_length = message_length
                while remaining_length > 0:
                    chunk = client_socket.recv(remaining_length)
                    if not chunk:
                        break
                    full_message += chunk
                    remaining_length -= len(chunk)
                if remaining_length > 0:
                    break
                cmd, request = full_message.decode('utf-8')[0], full_message.decode('utf-8')[1:]
                response = self.process_request(cmd, request)
                response_message = f"{len(response):03d}{response}".encode('utf-8')
                client_socket.sendall(response_message)
        except Exception as e:
            print(f"Error handling client: {e}" )
        finally:
            client_socket.close()
            print(f"Connection closed")
        
    def process_request(self, cmd, request):
        self.state["total_operations"] += 1
        response = ""
        try:
            with self.lock:
                self.state["total_operations"] += 1
                if cmd == "R":
                    key = request
                    if key in self.tuple:
                        value = self.tuple[key]
                        response = f"OK ({key} {value}) read"
                        self.state["READs"] += 1
                    else:
                        response = f"ERR {key} does not exist"
                        self.state["errors"] += 1
                elif cmd == "G":
                    key = request
                    if key in self.tuple:
                        value = self.tuple.pop(key)
                        response = f"OK ({key} {value}) removed"
                        self.state["GETs"] += 1

                        self.state["numtuples"] -= 1
                        self.state["avertuple"] -= (len(key)+len(value))
                        self.state["averkey"] -= len(key)
                        self.state["avervalue"] -= len(value)             
                    else:
                        response = f"ERR {key} does not exist"
                        self.state["errors"] += 1
                elif cmd == "P":            
                    if ' ' not in request:
                        self.state["errors"] += 1
                        response = "ERR invalid format"
                    else:
                        key, value = request.split(" ",1)
                        if len(key) +len(value) > 970 :
                            response = "ERR size exceeded"
                            self.state["errors"] += 1
                        elif key in self.tuple:
                            response = f"ERR {key} already exists"
                            self.state["errors"] += 1
                        else:
                            self.tuple[key] = value
                            response = f"OK ({key} {value}) added"
                            self.state["PUTs"] += 1
                            self.state["numtuples"] += 1
                            self.state["avertuple"] += len(key) + len(value)
                            self.state["averkey"] += len(key)
                            self.state["avervalue"] += len(value)
                return response
        except Exception as e:
            self.state["errors"] += 1
            response = f"Error processing request: {e}"
        
        
                
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
    Server()
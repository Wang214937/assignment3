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
        try:
            while True:
                client_socket, addr = server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,addr))
                client_thread.start()
        except KeyboardInterrupt:
            print("Server is shutting down...")
        finally:
            server_socket.close()

    def handle_client(self,client_socket, addr):
        print(f"New client connected from {addr}")
        while True:
            try:
                message = client_socket.recv(3).decode()
                print(f"client says: {message}")
                response = "Message received"
                client_socket.send(response.encode('utf-8'))
            except Exception as e:
                print(f"Error handling client{addr}: {e}" )
            finally:
                client_socket.close()
                print(f"Client {addr} closed")
        

    
if __name__ == "__main__":
    start_sever = Server()
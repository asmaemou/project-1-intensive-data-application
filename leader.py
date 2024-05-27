import socket

def leader():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('10.121.26.23', 5007))  # Bind to all interfaces
    server_socket.listen(5)
    print("Server listening on port 5007")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        
        # Send some data to the follower (example data)
        with open("follower_dump.sql", "wb") as file:
            data = file.read()
            client_socket.sendall(data)
        
        client_socket.close()

if __name__ == "__main__":
    leader()

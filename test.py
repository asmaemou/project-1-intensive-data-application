import socket
import os

def create_mysql_dump():
    username = 'asmaemouradi'
    password = 'password'
    database_name = 'intensive_data_base'
    dump_command = f"mysqldump -u {username} -p{password} {database_name} > follower_dump.sql"
    os.system(dump_command)

def leader():
    # Create the database dump
    create_mysql_dump()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('10.121.26.23', 5007))  # Bind to the specified address and port
    server_socket.listen(5)
    print("Server listening on port 5007")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        
        # Check if the file exists before opening
        if os.path.exists("follower_dump.sql"):
            with open("follower_dump.sql", "rb") as file:
                data = file.read()
                client_socket.sendall(data)
        else:
            print("File follower_dump.sql does not exist.")
        
        client_socket.close()

if __name__ == "__main__":
    leader()

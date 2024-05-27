import socket
import os

DB_USERNAME = 'asmaemouradi'
DB_PASSWORD = 'password'
DB_NAME = 'follower'
DB_HOST = 'localhost'
DB_PORT = '5432'

def restore_database(data):
    with open("follower_dump.sql", "wb") as file:
        file.write(data)
    os.environ['PGPASSWORD'] = DB_PASSWORD
    os.system(f"psql -U {DB_USERNAME} -d {DB_NAME} -f follower_dump.sql")
    os.remove("follower_dump.sql")

def follower(server_ip):
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, 5007))
            print(f"Connected to leader at {server_ip} on port 5007")
            data = b""
            while True:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                data += packet
            restore_database(data)
            client_socket.close()
        except ConnectionRefusedError as e:
            print(f"Connection failed: {e}")
            break

if __name__ == "__main__":
    server_ip = '10.121.26.23'  # Replace with the actual IP address of the server
    follower(server_ip)

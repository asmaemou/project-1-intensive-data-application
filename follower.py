import socket
import os
DB_USERNAME = 'user1234'
DB_PASSWORD = 'pass@1234'
DB_NAME = 'CITIES'
DB_HOST = 'localhost'
DB_PORT = '5432'

def restore_database(data):
    with open("follower_dump.sql", "wb") as file:
        file.write(data)
    os.environ['PGPASSWORD'] = DB_PASSWORD
    os.system(f"psql -U {DB_USERNAME} -d {DB_NAME} -f follower_dump.sql")
    os.remove("follower_dump.sql")
def follower():
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 5002))
        print("Connected to leader on port 5002")
        data = b""
        while True:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet
        restore_database(data)
        client_socket.close()
if __name__ == "__main__":
    follower()


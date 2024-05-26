import socket
import os
import psycopg2
import select
DB_USERNAME = 'asmaemouradi'
DB_PASSWORD = 'password'
DB_NAME = 'intensive data application'
DB_HOST = '10.126.14.44'
DB_PORT = '5432'
def dump_database():
    os.environ['PGPASSWORD'] = DB_PASSWORD
    os.system(f"pg_dump -U {DB_USERNAME} -d {DB_NAME} -f leader_dump.sql")
def send_update():
    with open("leader_dump.sql", "rb") as file:
        data = file.read()
    return data
def leader():
    conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host="localhost",
    port=DB_PORT
)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("LISTEN new_record;")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 5002))
    server_socket.listen(1)
    print("Leader listening on port 5002")
    while True:
        if select.select([conn], [], [], 5) == ([], [], []):
            continue
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            print(f"Received notification: {notify.payload}")
            dump_database()
            data = send_update()
            client_socket, address = server_socket.accept()
            print(f"Connection from {address}")
            client_socket.sendall(data)
            client_socket.close()
if __name__ == "__main__":
    leader()

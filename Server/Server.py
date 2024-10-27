import socket
import config
import threading
from API import Log
import ClientHandler

sock = socket.socket()
sock.bind((config.host.split(":")[0], int(config.host.split(":")[1]))) # ip, port
sock.listen(10)

while True:
    try:
        conn, addr = sock.accept()
        ip, port = addr
        addr = f"{ip}:{port}"
        Log.info(f"Client {addr} connected.")
        threading.Thread(target=lambda:ClientHandler.ClientHandler(addr, conn)).start()
    except Exception as ex:
        Log.error(ex)

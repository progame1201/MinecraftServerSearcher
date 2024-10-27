import socket
import uuid
import config


class User:
    def __init__(self, ip: str, conn: socket.socket):
        self.filters = config.Filters
        self.ip = ip
        self.conn = conn
        self.id = uuid.uuid4()
        self.started_scan = False

import socket
import threading
import time
from time import sleep
import Utils
import mcstatus
from API import Log, Filters, Servers, ScanEnded
from User import User
from ScanMethods.Ranges import DefaultRange


class Scan:
    def __init__(self, user: User):
        self.range = None
        self.method = None
        self.user: User = user
        self.found_servers = []
        self.ended_scans = 0
        self.filter: Filters = user.filters
        self.stop = False

    def servers_sender(self):
        while not self.stop:
            self.user.conn.send(Servers(self.found_servers).serialize())
            self.found_servers = []

            if self.ended_scans >= self.range.servers_count:
                self.user.conn.send(ScanEnded().serialize())
                self.stop = True
                return
            sleep(10)


    def defaultScan(self):
        self.range:DefaultRange
        ip = self.range.ip
        latter = self.range.server_name_latter
        servers_count = self.range.servers_count
        threading.Thread(target=self.servers_sender).start()
        for i in range(servers_count):
            if self.stop:
                break
            threading.Thread(target=lambda: self.scan_ip(f"{latter}{i+1}{ip}", self.range.port_range)).start()
        while not self.stop:
            time.sleep(1)
        return True

    def scan_ip(self, ip, port_range):
        start_port, end_port = port_range

        for i in range(start_port, end_port+1):
            if self.stop:
                break
            threading.Thread(target=self._check(ip, i)).start()
            sleep(self.filter.scan_speed)

        self.ended_scans += 1

    def _check(self, ip, port):
        try:
            server = mcstatus.JavaServer.lookup(f"{ip}:{port}", timeout=1.5)
            server.status()
            status = server.status()
            motd = status.motd.to_minecraft().replace("\n", " ")
            if Utils.found_filter(motd, status.players.online, self.filter.motd_pattern, status.version.name, self.filter.version_pattern, self.filter.online_filter):
                Log.info(f"Found server: {motd} ({status.version.name}) {status.players.online}/{status.players.max}")
                self.found_servers.append(f"{ip}:{port}")
        except:
            pass

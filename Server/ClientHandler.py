import socket
import config
import threading
import Scan
from ScanMethods import Default, methods
from API import Log, NetworkObject, Auth, StartScan, AdminSettings, Queue, StartedScan, Methods
from User import User

users: list[User] = []
_methods_dict = {}
for method in methods:
    if isinstance(method, Default):
        _methods_dict[method.name] = [{_range.name: f"{_range.name.split("_")[1]}{_range.servers_count}{_range.ip}"} for _range in method.ranges]
_methods = Methods(_methods_dict).serialize()
scans: dict[User, list[Scan.Scan]] = {}


class ClientHandler:
    def __init__(self, ip, conn):
        self.user: User = User(ip, conn)
        self.user.filters = config.default_filters
        self.conn: socket.socket = conn
        self._auth()

    def _disconnect(self):
        self.conn.close()
        if self.user:
            Log.info(f"Disconnected {self.user.id} ({self.user.ip})")
        if self.user in users:
            users.remove(self.user)
        if self.user in list(scans.keys()):
            for scan in scans[self.user]:
                scan.stop = True
            del scans[self.user]

    def _auth(self):
        try:
            data = self.conn.recv(1024)
            if not data:
                raise TypeError("data is None")
            if self.HandleObject(NetworkObject.deserialize(data)):  #netobj must be Auth
                users.append(self.user)
                self.conn.send(_methods)
                Log.info(f"User {self.user.id} ({self.user.ip}) authenticated")
                self._receiver()
                return
        except Exception as ex:
            Log.error(ex)
            self._disconnect()

    def _receiver(self):
        try:
            while True:
                data = self.conn.recv(1024 * 8)  #8 kb
                if not data:
                    raise TypeError("data is None")
                self.HandleObject(NetworkObject.deserialize(data))
        except Exception as ex:
            Log.error(ex)
            self._disconnect()

    def HandleObject(self, netobj: NetworkObject):
        try:
            method = None
            range = None

            if isinstance(netobj, Auth):
                Log.info(f"Received Auth from {self.user.id} ({self.user.ip})")
                if netobj.passcode == config.client_passcode:
                    return True
                return False

            if isinstance(netobj, StartScan):
                Log.info(f"Received StartScan from {self.user.id} ({self.user.ip})")
                if self.user in scans.keys():
                    if len(scans[self.user]) >= config.limit_by_user:
                        self.conn.send(Queue().serialize())
                        return 
                if len(list(scans.keys())) >= config.max_scans:
                    self.conn.send(Queue().serialize())
                    return

                for method in methods:
                    if method.name != netobj.method_name:
                        continue
                    break

                if not method:
                    return

                for range in method.ranges:
                    if range.name != netobj.range_name:
                        continue
                    break

                if not range:
                    return
                scan = Scan.Scan(self.user)

                if isinstance(method, Default):
                    scan.method = method
                    scan.range = range
                    threading.Thread(target=lambda: scan.defautlScan()).start()
                if self.user in scans.keys():
                    scans[self.user].append(scan)
                else:
                    scans[self.user] = [scan]

                self.conn.send(StartedScan().serialize())

                return True

            if isinstance(netobj, AdminSettings):
                Log.info(f"Received AdminSettings from {self.user.id} ({self.user.ip})")
                if netobj.password != config.admin_password:
                    return False
                self.user.filters = netobj.filters
                return True
            return False
        except Exception as ex:
            Log.error(ex)
            self._disconnect()

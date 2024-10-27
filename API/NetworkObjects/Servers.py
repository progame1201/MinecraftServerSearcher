from .NetworkObject import NetworkObject

class Servers(NetworkObject):
    def __init__(self, servers):
        super().__init__()
        self.servers = servers

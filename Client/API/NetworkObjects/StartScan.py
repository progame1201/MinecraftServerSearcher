from .NetworkObject import NetworkObject

class StartScan(NetworkObject):
    def __init__(self, range_name, method_name):
        super().__init__()
        self.range_name = range_name
        self.method_name = method_name

from .NetworkObject import NetworkObject

class Methods(NetworkObject):
    def __init__(self, methods):
        super().__init__()
        self.methods:dict[str:list[str]] = methods #method name:range names

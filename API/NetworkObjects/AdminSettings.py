from .NetworkObject import NetworkObject
from API import Filters

class AdminSettings(NetworkObject):
    def __init__(self, filters, password):
        super().__init__()
        self.password = password
        self.filters:Filters = filters

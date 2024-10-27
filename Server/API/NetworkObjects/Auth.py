from .NetworkObject import NetworkObject

class Auth(NetworkObject):
    def __init__(self, passcode):
        super().__init__()
        self.passcode = passcode

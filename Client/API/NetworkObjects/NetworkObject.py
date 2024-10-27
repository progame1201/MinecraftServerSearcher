import pickle

class NetworkObject:
    def __init__(self):
        pass
    def serialize(self):
        return pickle.dumps(self)
    @staticmethod
    def deserialize(data):
        return pickle.loads(data)
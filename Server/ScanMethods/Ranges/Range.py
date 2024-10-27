class Range:
    def __init__(self, port_range, servers_count, name, ip="127.0.0.1", ip_range=("127.0.0.1", "127.0.0.1")):
        self.name = name
        self.ip = ip
        self.ip_range = ip_range
        self.port_range = port_range
        self.servers_count = servers_count
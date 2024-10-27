from .Range import Range
class DefaultRange(Range):
    def __init__(self, server_name_latter, port_range, servers_count, name, ip="127.0.0.1", ip_range=("127.0.0.1", "127.0.0.1")):
        super().__init__(port_range, servers_count, name, ip, ip_range)
        self.server_name_latter = server_name_latter
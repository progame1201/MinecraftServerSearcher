class Filters:
    def __init__(self, online_filter, motd_pattern, version_pattern, scan_speed):
        if version_pattern == "None":
            self.version_pattern = None
        else:
            self.version_pattern = version_pattern
        if motd_pattern == "None":
            self.motd_pattern = None
        else:
            self.motd_pattern = motd_pattern

        self.online_filter = online_filter
        self.scan_speed = scan_speed
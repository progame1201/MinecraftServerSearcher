from .Method import Method
from .Ranges import DefaultRange
class Default(Method):
    def __init__(self):
        super().__init__()
        self.name = self.__class__.__name__
        self.ranges = [
            DefaultRange("wa", (25000, 30000), 5, "JR_WA", ".joinserver.ru"),
            DefaultRange("w", (25000, 30000), 1, "JR_W", ".joinserver.ru"),
            DefaultRange("n", (25000, 30000), 28, "JR_N", ".joinserver.ru"),
            DefaultRange("f", (25000, 30000), 28, "JR_F", ".joinserver.ru"),
            DefaultRange("m", (25000, 30000), 32, "JR_M", ".joinserver.ru"),
            DefaultRange("s", (25000, 30000), 31, "JR_S", ".joinserver.ru"),
            DefaultRange("z", (25000, 30000), 28, "JR_Z", ".joinserver.ru"),

            DefaultRange("f", (20000, 30000), 9, "GP_F", ".gamely.pro"),
            DefaultRange("d", (20000, 30000), 34, "GP_D", ".gamely.pro"),
            DefaultRange("g", (20000, 30000), 11, "GP_G", ".gamely.pro"),

            DefaultRange("f", (20000, 40000), 1, "RM_F", ".rustix.me"),
            DefaultRange("d", (20000, 26000), 4, "RM_D", ".rustix.me"),

            DefaultRange("n", (25000, 30000), 32, "JX_N", ".joinserver.xyz"),
            DefaultRange("s", (25000, 30000), 32, "JX_S", ".joinserver.xyz"),
            DefaultRange("z", (25000, 30000), 28, "JX_Z", ".joinserver.xyz"),
            DefaultRange("f", (25000, 30000), 32, "JX_F", ".joinserver.xyz"),
            DefaultRange("m", (25000, 30000), 32, "JX_M", ".joinserver.xyz"),
            DefaultRange("br", (25000, 30000), 2, "JX_BR", ".joinserver.xyz"),
            DefaultRange("wa", (25000, 30000), 13, "JX_WA", ".joinserver.xyz"),
            DefaultRange("lim", (25000, 30000), 10, "JX_LIM", ".joinserver.xyz"),
            DefaultRange("fsn", (25000, 30000), 12, "JX_FSN", ".joinserver.xyz"),

            DefaultRange("f", (19000, 26000), 2, "VN_F", ".veroid.net"),
            DefaultRange("g", (19000, 26000), 5, "VN_G", ".veroid.net"),
            DefaultRange("e", (19000, 26000), 2, "VN_E", ".veroid.net"),
        ]
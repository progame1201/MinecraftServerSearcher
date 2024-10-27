from datetime import datetime
from colorama import Fore, init
from typing import Any
init(True)

class Log():
    @staticmethod
    def info(string:Any, end:Any="\n"):
        print(f"[{datetime.now()}] {string}", end=end)

    @staticmethod
    def error(string:Any, end:Any="\n"):
        print(f"{Fore.RED}[{datetime.now()}] [ERROR] {string}", end=end)
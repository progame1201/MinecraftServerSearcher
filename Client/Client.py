import socket
import threading
import NBTFileUtils as Utils
from PyQt6 import uic
import config
import os
from API import Log, NetworkObject, Auth, StartScan, AdminSettings, Queue, StartedScan, Methods, Filters, Servers, ScanEnded
import sys
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import QThread, QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QSpinBox, QTextBrowser, QLineEdit, QPushButton, QComboBox
from time import sleep


class receiver(QObject):
    set_text = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.servers_queue = []

    def receiver(self):
        threading.Thread(target=self.queue).start()
        try:
            while True:
                data = sock.recv(4096 * 8)
                if not data:
                    return
                self.handle_object(NetworkObject.deserialize(data))
        except Exception as ex:
            print(ex)

    def queue(self):
        while True:
            try:
                added_servers = 0
                servers_count = len(self.servers_queue)
                if len(self.servers_queue) == 0:
                    continue
                for server in self.servers_queue:
                    if Utils.add_server_to_minecraft(server, config.path_to_minecraft_servers, server):
                        added_servers += 1

                self.servers_queue = []

                self.set_text.emit(f"Received servers. {added_servers}/{servers_count} servers added")

                sleep(10)
            except Exception as ex:
                print(ex)

    def handle_object(self, netobj: NetworkObject):

        if isinstance(netobj, StartedScan):
            self.set_text.emit("started scan!")

        if isinstance(netobj, Servers):
            print(netobj.servers)
            self.servers_queue.extend(netobj.servers)

        if isinstance(netobj, Queue):
            self.set_text.emit("queue. retry start latter.")

        if isinstance(netobj, ScanEnded):
            self.set_text.emit("Scan ended!")


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(f'ui.ui', self)

        self.thread = QThread()
        self.worker = receiver()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.receiver)
        self.thread.started.connect(self.worker.queue)

        self.worker.set_text.connect(self.log)
        self.thread.start()

        self.status_box: QTextBrowser
        self.scan_speed: QLineEdit
        self.online: QSpinBox
        self.ver: QLineEdit
        self.nameregex: QLineEdit
        self.pushButton: QPushButton  # start button
        self.Methods: QComboBox
        self.Ranges: QComboBox
        self.save: QPushButton  # send admin settings

        self.Warn.hide()
        self.settings_hidden.hide()

        if config.admin_password == None:
            self.setting.hide()
            self.settings_hidden.show()

        if not os.path.exists(config.path_to_minecraft_servers):
            self.Warn.show()

        for method in methods.keys():
            self.Methods.addItem(method)

        for range in methods[list(methods.keys())[0]]:
            self.Ranges.addItem(list(range.values())[0])

        self.Methods.currentTextChanged.connect(self.reload_ranges)
        self.status_box.textChanged.connect(lambda: self.status_box.moveCursor(QTextCursor.MoveOperation.End))
        self.save.clicked.connect(self.send_admin_settings)
        self.pushButton.clicked.connect(self.start)

    def reload_ranges(self, text):
        for range in methods[methods[text]]:
            self.Ranges.addItem(list(range.values())[0])
    def log(self, text):
        try:
            if len(self.status_box.toPlainText()) == 0:
                self.status_box.setText(text)
                return
            self.status_box.setText(f"{self.status_box.toPlainText()}\n{text}")
        except Exception as ex:
            print(ex)

    def start(self):
        try:
            _range = None

            for range_list in methods.values():
                for range in range_list:
                    if list(range.values())[0] == self.Ranges.currentText():
                        _range = list(range.keys())[0]

            sock.send(StartScan(_range, self.Methods.currentText()).serialize())
        except Exception as ex:
            print(ex)

    def send_admin_settings(self):
        try:
            sock.send(AdminSettings(Filters(self.online.value(), self.nameregex.text(), self.ver.text(), float(self.scan_speed.text())), config.admin_password).serialize())
            self.log("Admin settings saved.")
        except Exception as ex:
            self.log(f"Please, enter a valid data to admin settings.\n{ex}")


if __name__ == "__main__":
    sock = socket.socket()
    sock.connect((config.host.split(":")[0], int(config.host.split(":")[1])))
    sock.send(Auth(config.passcode).serialize())
    methods: dict[str:list[str]] = NetworkObject.deserialize(sock.recv(4096 * 4)).methods

    #print(methods)

    app = QApplication(sys.argv)
    ex = App()
    app.setStyle('windows11')
    ex.show()
    sys.exit(app.exec())

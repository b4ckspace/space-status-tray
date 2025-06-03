#!/usr/bin/python

try:
    from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
    from PySide6.QtGui import QIcon, QDesktopServices, QAction
    from PySide6 import QtCore, QtGui, QtNetwork
    from PySide6.QtCore import QTimer
except:
    print("Using PyQt5")
    from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
    from PyQt5.QtGui import QIcon, QDesktopServices
    from PyQt5 import QtCore, QtGui, QtNetwork
    from PyQt5.QtCore import QTimer

import json

class SpaceStatus:

    def __init__(self):

        self.app = app = QApplication([])
        app.setQuitOnLastWindowClosed(False)

        self.icons = [QIcon("icons/backspace-closed.svg")]
        for i in range(1, 21):
            self.icons.append(QIcon(f"icons/backspace-open-{i}.svg"))
        self.icons.append(QIcon(f"icons/backspace-open-2X.svg"))
        self.icons.append(QIcon.fromTheme("user-offline"))

        self.trayicon = tray = QSystemTrayIcon()
        tray.setIcon(self.icons[-1])
        tray.setVisible(True)
        tray.activated.connect(self.doActivation)

        menu = QMenu()
        action = QAction("Quit")
        menu.addAction(action)
        action.triggered.connect(app.quit)

        tray.setContextMenu(menu)

        self.timer=QTimer()
        self.timer.timeout.connect(self.doRequest)
        self.timer.start(20*60*1000)
        
        self.doRequest()

        app.exec()

    def doActivation(self, reason):
        if reason == self.trayicon.ActivationReason.MiddleClick: # middle mouse clicked
            QDesktopServices.openUrl(QtCore.QUrl("https://www.hackerspace-bamberg.de"))
        elif reason == self.trayicon.ActivationReason.Trigger:
            self.trayicon.setIcon(self.icons[-1])
            self.doRequest()

    def doRequest(self):   

        url = "https://status.bckspc.de/spacestatus.php"
        req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))

        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)
        self.nam.get(req)
      
    def handleResponse(self, reply):

        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:
    
            try:
                bytes_string = reply.readAll()
                data = json.loads(str(bytes_string, 'utf-8'))
                number = data["sensors"]["people_now_present"][0]["value"]
                names = data["sensors"]["people_now_present"][0].get("names", [])
            except: # XXX
                number = 0
                names = ["ERROR"]

            names_dict = {}
            for n in names:
                names_dict.setdefault(n, 0)
                names_dict[n] += 1

            num_names = len(names)
            display_names = [n if names_dict[n] <= 1 else f"{n} ({names_dict[n]}x)" for n in sorted(names_dict.keys())]

            self.trayicon.setIcon(self.icons[min(number, 21)])
            self.trayicon.setToolTip(", ".join(display_names))
            #print(number, names)
        else:
            print("Error occured: ", er)
            print(reply.errorString())


if __name__ == '__main__':
    app = SpaceStatus()

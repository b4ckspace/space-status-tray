#!/usr/bin/python

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
        for i in range(1, 10):
            self.icons.append(QIcon(f"icons/backspace-open-{i}.svg"))
        self.icons.append(QIcon(f"icons/backspace-open-1X.svg"))
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
                names = data["sensors"]["people_now_present"][0]["names"]
            except: # XXX
                number = 0
                names = ["ERROR"]

            self.trayicon.setIcon(self.icons[min(number, 10)])
            self.trayicon.setToolTip(", ".join(names))
            #print(number, names)
        else:
            print("Error occured: ", er)
            print(reply.errorString())


if __name__ == '__main__':
    app = SpaceStatus()

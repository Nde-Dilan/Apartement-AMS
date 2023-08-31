from PyQt5.QtWidgets import QMainWindow

from PyQt5.QtWidgets import *
import qdarktheme
import sys

import MySQLdb

from PyQt5.uic import loadUiType

ui, _ = loadUiType("login.ui")
light = True
login = False


def toggle_theme():
    global light
    if light:
        qdarktheme.setup_theme()
        light = False
    else:
        qdarktheme.setup_theme("light")
        light = True

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_buttons()

    def handle_buttons(self):
        self.logBtn.clicked.connect(self.login)
        self.quitBtn.clicked.connect(self.close)
        self.sunBtn.clicked.connect(toggle_theme)

    def login(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        username = self.username.text()
        password = self.password.text()
        print(username)
        if username != '' and password != '':
            try:
                self.cursor.execute('''
                        SELECT * FROM users WHERE username = (%s)
                        ''', (username,))
                user = self.cursor.fetchone()
                print(user)
                if user is None or user[2] != password:
                    QMessageBox.warning(self, "Warning", "Invalid password!", QMessageBox.Ok)
                else:
                    global login
                    login = True
                    self.close()
            except Exception as e:
                print(e)
        else:
            QMessageBox.warning(self, "Warning", "Please enter a username and a password!", QMessageBox.Ok)

        print(password)

    # self.cursor.execute('''SELECT * FROM users WHERE username = (%s) AND password= (%s)
    #                                  ''', (username, password,))
    # ask the user to enter a username and a password , just the admin can login to the software, the admin can add other users through the form


def main_login():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("light")
    window = MainApp()
    window.show()
    app.exec_()
    return login

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qdarktheme
import sys
#TODO :Make the scroll bar functional, test the send_mail functionality, design the db
#TODO :add a new tenant, make the combo box of the status readonly
#TODO : Click on one room open the second tab with all the info of that room
#TODO: Clean the code
from login import main_login, toggle_theme

import MySQLdb

from PyQt5.uic import loadUiType

ui, _ = loadUiType("library.ui")
light = True


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # self.fill_book_db()
        self.handle_ui_changes()
        self.handle_buttons()
        self.show_emails()
        self.show_subjects()

    def handle_ui_changes(self):
        self.tabWidget.tabBar().setVisible(False)

    def handle_buttons(self):
        self.dayBtn.clicked.connect(self.open_day_to_day_tab)
        self.themeBtn.clicked.connect(toggle_theme)
        view_tenant_btns = [self.view_tenant_btn,self.view_tenant_btn_2,self.view_tenant_btn_3,self.view_tenant_btn_4,self.view_tenant_btn_5,self.view_tenant_btn_6,self.view_tenant_btn_7,self.view_tenant_btn_8,self.view_tenant_btn_9,self.view_tenant_btn_10]
        for view_tenant in view_tenant_btns:
            view_tenant.clicked.connect(self.open_tenant_view)
        self.bookBtn.clicked.connect(self.open_books_tab)
        self.userBtn.clicked.connect(self.open_users_tab)
        self.settingBtn.clicked.connect(self.open_settings_tab)
        # operations
        self.addUserBtn.clicked.connect(self.add_new_user)
        self.saveChangesUser.clicked.connect(self.update_user)
        self.loginBtn.clicked.connect(self.edit_user)
        self.sendEmailBtn.clicked.connect(self.send_email)

    #####################################################
    ############### opening tabs ######################

    def open_day_to_day_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_books_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_users_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_settings_tab(self):
        self.tabWidget.setCurrentIndex(3)


    ##### Differents functionalities ######

    def send_email(self):
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication

        # Email configuration
        sender_email = self.sender_email.text()
        sender_password = self.my_password.text()
        recipient_email = self.recipient_email()
        subject = self.subject.currentText()
        body = self.contentEmail.toPlainText()

        # SMTP server settings (for Gmail)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create the MIME message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))


        # Establish a secure connection and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        QMessageBox.Information(self, "Info", "Email sent successfully!", QMessageBox.Ok)

    def open_tenant_view(self):
        self.open_books_tab()
    #####################################################
    ############### user operations ######################

    def add_new_user(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='apartement')
        self.cursor = self.db.cursor()

        username = self.username.text()
        email = self.email.text()
        move_in = self.move_in.date().toString("yyyy-MM-dd")

        tenant = self.cursor.execute('''
                       SELECT * FROM tenant WHERE name = (%s)
                       ''', (username,))
        print(tenant)

        if tenant:
            # open a dialog box to say that the username is already taken
            pass
        else:
            if username and email :
                self.cursor.execute('''
                            INSERT INTO tenant (name, email, move_in)
                            VALUES (%s, %s, %s)
                            ''', (username, email, move_in))
                self.db.commit()
                self.db.close()
                QMessageBox.information(self, "Info", "The user has been added successfully!", QMessageBox.Ok)

            else:
                # Open the dialog box with the message
                print("Please don't create problem")

    # TODO Finish with the login functionality

    def show_emails(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='apartement')
        self.cursor = self.db.cursor()

        self.cursor.execute('''
          SELECT email FROM Tenant
          ''')

        data = self.cursor.fetchall()
        for email in data:
            self.emailCombo.addItem(email[0])
            print(email)

        self.db.commit()
        self.db.close()
    def show_subjects(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='apartement')
        self.cursor = self.db.cursor()

        self.cursor.execute('''
              SELECT subject FROM bills
              ''')

        data = self.cursor.fetchall()
        print(data)
        for subject in data:
            self.emailCombo.addItem(subject[0])
            print(subject)

        self.db.commit()
        self.db.close()

    def edit_user(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='apartement')
        self.cursor = self.db.cursor()

        username = self.username2.text()
        email = self.email_2.text()

        self.cursor.execute('''
                               SELECT * FROM tenant WHERE username = (%s) AND email= (%s)
                               ''', (username, email,))
        tenant = self.cursor.fetchone()
        #print(user)
        if tenant:
            change_visibility = [self.username3, self.email_3, self.move_in_3,
                                 self.saveChangesUser]

            for obj in change_visibility:
                obj.setEnabled(True)

            self.username3.setText(tenant[1])
            self.email_3.setText(tenant[2])
            self.move_in.setText(tenant[3])
        else:
            print("Please don't create problem")

    def update_user(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='apartement')
        self.cursor = self.db.cursor()

        new_username = self.username3.text()
        new_email = self.email_3.text()
        new_move_in = move_in.date().toString("yyyy-MM-dd")
        # date.fromString(date_string, "yyyy-MM-dd")


        username = self.username2.text()
        email = self.email.text()
        update_query = '''UPDATE users
                          SET username = %s , email=%s, move_in= %s,
                          WHERE username = %s'''

        if new_username and new_email and new_move_in:
            self.cursor.execute(update_query, (new_username, new_email, new_move_in, username,))
            self.db.commit()
            self.db.close()
            change_visibility = [self.username3, self.email_3, self.move_in_3,
                                 self.saveChangesUser]

            for obj in change_visibility:
                obj.setEnabled(False)
            self.statusBar().showMessage("The user has been updated successfully!")
        else:
            print("Please don't create problem")

    #####################################################
    ############### opening tabs ######################




def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("dark")
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    # login_=main_login()
    if True:
        main()
    else:
        pass
# run this inside the terminal to avoid the error caused by the .qrc file :

# pyrcc5 icons.qrc -o icons_rc.py

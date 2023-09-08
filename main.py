from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qdarktheme
import sys
pass_key = "auavzkcycnhdmjmk"
#TODO :Create a button to open a matplotlib graph out of the pyqt5 app
# TODO: Reliability of a client
#TODO :add a new tenant, make the combo box of the status readonly
#TODO : Click on one room open the second tab with all the info of that room
#TODO: Clean the code
from login import main_login, toggle_theme

import MySQLdb

from PyQt5.uic import loadUiType

ui, _ = loadUiType("library.ui")

light = True
tenant_id=0

# draw_graph()
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
        self.seeTheGraph.clicked.connect(self.draw_graph)
        self.dayBtn.clicked.connect(self.open_tenants_tab)
        self.themeBtn.clicked.connect(toggle_theme)
        # view_tenant_btns = [self.view_tenant_btn,self.view_tenant_btn_2,self.view_tenant_btn_3,self.view_tenant_btn_4,self.view_tenant_btn_5,self.view_tenant_btn_6,self.view_tenant_btn_7,self.view_tenant_btn_8,self.view_tenant_btn_9,self.view_tenant_btn_10]
        # for view_tenant in view_tenant_btns:
        #     view_tenant.clicked.connect(lambda : self.open_tenant_view(view_tenant_btns.index(view_tenant)))
        view_tenant_btns = [self.view_tenant_btn, self.view_tenant_btn_2, self.view_tenant_btn_3,
                            self.view_tenant_btn_4, self.view_tenant_btn_5, self.view_tenant_btn_6,
                            self.view_tenant_btn_7, self.view_tenant_btn_8, self.view_tenant_btn_9,
                            self.view_tenant_btn_10]

        [view_tenant.clicked.connect(lambda _, index=view_tenant_btns.index(view_tenant): self.open_tenant_view(index)) for view_tenant in view_tenant_btns]

        self.bookBtn.clicked.connect(self.open_tenant_details)
        self.userBtn.clicked.connect(self.open_users_tab)
        self.settingBtn.clicked.connect(self.open_email_tab)
        self.send_email.clicked.connect(self.open_email_tab)
        # operations
        self.addUserBtn.clicked.connect(self.add_new_user)
        self.saveChangesUser.clicked.connect(self.update_user)
        self.loginBtn.clicked.connect(self.edit_user)

        self.sendEmailBtn_2.clicked.connect(self.send_email_func)
        self.quitMailBtn_2.clicked.connect(self.open_tenants_tab)
        self.backBtn.clicked.connect(self.open_tenants_tab)

    #####################################################
    ############### opening tabs ######################

    def open_tenants_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_tenant_details(self):
        self.tabWidget.setCurrentIndex(1)

    def open_users_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_email_tab(self):
        self.tabWidget.setCurrentIndex(3)


    ##### Differents functionalities ######

    def send_email_func(self):
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication

        # Email configuration
        sender_email = self.sender_email.text()
        sender_password = self.my_password.text()
        recipient_email = self.emailCombo.currentText()
        subject = self.subjectCombo.currentText()
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

        QMessageBox.information(self, "Info", "Email sent successfully!", QMessageBox.Ok)

    def draw_graph(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='apartement')
        self.cursor = self.db.cursor()
        import matplotlib.pyplot as plt

        global tenant_id
        room_id = tenant_id
        self.cursor.execute('''
                                           SELECT payement_history FROM tenants WHERE room_id = (%s)
                                           ''', (room_id,))
        data = self.cursor.fetchone()
        print("data")
        print(data)
        import ast
        payment_status = ast.literal_eval(data[0])

        # Months (x-axis)
        months = ["Month 1", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6"]

        # Create a bar graph
        plt.bar(months, payment_status, color=['green' if status == 'Yes' else 'red' for status in payment_status])

        # Set labels and title
        plt.xlabel("Months")
        plt.ylabel("Payment Status")
        plt.title("Client Payment Status Over 6 Months")

        # Display the graph
        plt.show()

    def is_reliable(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='apartement')
        self.cursor = self.db.cursor()

        global tenant_id
        room_id = tenant_id
        self.cursor.execute('''
                                                   SELECT payement_history FROM tenants WHERE room_id = (%s)
                                                   ''', (room_id,))
        payment_status = self.cursor.fetchone()
        print(payment_status)
        reliability_criteria = 5
        import ast

        # Calculate the client's reliability based on payment history
        num_payments = ast.literal_eval(payment_status[0]).count("Yes")

        # Make a determination
        if num_payments >= reliability_criteria:
            self.reliability.setText("Reliable")
        else:
            self.reliability.setText("Unreliable")



    def open_tenant_view(self,id):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='apartement')
        self.cursor = self.db.cursor()
        global tenant_id
        tenant_id=id+1
        room_id = id+1
        self.is_reliable()
        try:
            data= self.cursor.execute('''
                                   SELECT * FROM tenants WHERE room_id = (%s)
                                   ''', (room_id,))


        except Exception as e:
            print(e)

        data1 = self.cursor.fetchone()
        print(data1)

        self.name_label.setText("Name : "+data1[1])
        self.email_label.setText("Email : "+data1[2])

        # print(id)
        self.open_tenant_details()
    #####################################################
    ############### user operations ######################

    def add_new_user(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='apartement')
        self.cursor = self.db.cursor()

        username = self.username.text()
        email = self.email.text()
        move_in = self.move_in.date().toString("yyyy-MM-dd")

        tenant = self.cursor.execute('''
                       SELECT * FROM tenants WHERE name = (%s)
                       ''', (username,))
        # print(tenant)

        if tenant:
            # open a dialog box to say that the username is already taken
            pass
        else:
            if username and email :
                self.cursor.execute('''
                            INSERT INTO tenants (name, email, move_in)
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
          SELECT email FROM tenants
          ''')

        data = self.cursor.fetchall()
        for email in data:
            self.emailCombo.addItem(email[0])
            # print(email)

        self.db.commit()
        self.db.close()
    def show_subjects(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='apartement')
        self.cursor = self.db.cursor()

        self.cursor.execute('''
              SELECT subject FROM bills
              ''')

        data = self.cursor.fetchall()


        self.db.commit()
        self.db.close()

    def edit_user(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='apartement')
        self.cursor = self.db.cursor()

        username = self.username2.text()
        email = self.email_2.text()

        self.cursor.execute('''
                               SELECT * FROM tenants WHERE username = (%s) AND email= (%s)
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

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


# TODO: Create a global variable to handle user and admin, like is_admin, regler le pb avec les combo box et continuer avec la 1ere page


def db_manager(self):
    self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
    self.cursor = self.db.cursor()




class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # self.fill_book_db()
        self.handle_ui_changes()
        self.handle_buttons()
        self.show_emails()
        self.show_subjects()


    def fill_book_db(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        insert_query = '''
        INSERT INTO book (title, author, category, available, number_of_pages,description,language)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        book_list = [
            ("To Kill a Mockingbird", "Harper Lee", "Fiction", 1, 336,
             "A classic novel tackling issues of race and morality in the American South.", "English"),
            ("1984", "George Orwell", "Fiction", 1, 328,
             "A dystopian masterpiece exploring surveillance and totalitarianism.", "English"),
            ("Pride and Prejudice", "Jane Austen", "Fiction", 1, 432,
             "A timeless tale of love and social norms in Regency-era England.", "English"),
            ("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 1, 180,
             "A vivid portrayal of the Jazz Age's excesses and the American Dream.", "English"),
            ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 1, 320,
             "The magical start to a beloved series about a young wizard's adventures.", "English"),
            ("The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 1, 1178,
             "An epic journey through a world of hobbits, elves, and dark forces.", "English"),
            ("The Catcher in the Rye", "J.D. Salinger", "Fiction", 1, 277,
             "A coming-of-age story capturing the disillusionment of a teenage boy.", "English"),
            ("Animal Farm", "George Orwell", "Fiction", 1, 112,
             "A satirical allegory illustrating the dangers of political power struggles.", "English"),
            ("Brave New World", "Aldous Huxley", "Fiction", 1, 288,
             "A futuristic society explores themes of technology, conformity, and free will.", "English"),
            ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1, 310,
             "A charming adventure featuring a hobbit on a quest for treasure.", "English"),
            ("The Da Vinci Code", "Dan Brown", "Mystery", 1, 592,
             "A gripping thriller unraveling cryptic codes and historical secrets.", "English"),
            ("The Hunger Games", "Suzanne Collins", "Young Adult", 1, 374,
             "In a dystopian world, a fight for survival unfolds in a televised arena.", "English"),
            ("The Alchemist", "Paulo Coelho", "Fiction", 1, 208,
             "A philosophical journey of self-discovery and the pursuit of dreams.", "English"),
            ("Fahrenheit 451", "Ray Bradbury", "Science Fiction", 1, 249,
             "In a future society, firemen burn books to control knowledge and ideas.", "English"),
            ("Gone with the Wind", "Margaret Mitchell", "Fiction", 1, 960,
             "A sweeping historical romance set against the backdrop of the Civil War.", "English"),
        ]

        self.cursor.executemany(insert_query, book_list)
        self.db.commit()
        print("Data insertion successful.")

    def handle_ui_changes(self):
        self.tabWidget.tabBar().setVisible(False)

    def handle_buttons(self):
        self.dayBtn.clicked.connect(self.open_day_to_day_tab)
        self.themeBtn.clicked.connect(toggle_theme)

        self.deleteBook.clicked.connect(self.delete_book)
        self.bookBtn.clicked.connect(self.open_books_tab)
        self.userBtn.clicked.connect(self.open_users_tab)
        self.settingBtn.clicked.connect(self.open_settings_tab)
        # operations
        self.saveBtn.clicked.connect(self.add_new_book)
        self.addUserBtn.clicked.connect(self.add_new_user)
        self.saveChangesUser.clicked.connect(self.update_user)
        self.searchBtn.clicked.connect(self.search_book)
        self.loginBtn.clicked.connect(self.edit_user)
        self.sendEmailBtn.clicked.connect(self.send_email)
        # self.quitMailBtn.clicked.connect(self.update_user)
        self.saveChanges.clicked.connect(self.edit_book)

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

        print("Email sent successfully!")

    #####################################################
    ############### book operations ######################

    def add_new_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        book_title = self.book_title.text()
        book_author = self.book_author.text()
        category = self.category_combo.currentText()
        available = 0 if self.available_combo.currentText() == 'False' else 1
        pages = int(self.pages.text())
        description = self.description.toPlainText()
        language = self.language_combo.currentText()

        self.cursor.execute('''
            INSERT INTO book (title, author, category, available, number_of_pages, description, language)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (book_title, book_author, category, available, pages, description, language))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage("Book added successfully")

    def search_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        book_title = self.title_search.text()
        self.cursor.execute('''
        SELECT * FROM book WHERE title = (%s)
        ''', (book_title,))

        data = self.cursor.fetchall()
        # print(data)
        self.pagesEdit.setText(str(data[0][5]))
        self.titleEdit.setText(data[0][1])
        self.authorEdit.setText(data[0][2])
        self.descriptionEdit.setPlainText(data[0][6])
        self.categoryEdit.addItem(data[0][3])
        self.categoryEdit.setCurrentText(data[0][3])
        print("--------> : ",data[0][3],data[0][7])
        self.language_combo_2.addItem(data[0][7])
        self.language_combo_2.setCurrentText(data[0][7])
        self.availableEdit.setCurrentText("True" if data[0][4] == 1 else "False")
        self.db.commit()
        self.db.close()

    def edit_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()
        book_title = self.title_search.text()
        self.cursor.execute('''
                SELECT * FROM book WHERE title = (%s)
                ''', (book_title,))

        data = self.cursor.fetchall()

        update_query = '''
                    UPDATE book
                    SET title = %s, author = %s, category = %s,available = %s, number_of_pages = %s, description = %s, language=%s
                    WHERE title = %s'''

        pages = self.pagesEdit.text()

        title = self.titleEdit.text()
        author = self.authorEdit.text()
        description = self.descriptionEdit.toPlainText()
        category = self.categoryEdit.currentText()
        language = self.language_combo_2.currentText()
        print(self.availableEdit.currentText())
        available = 0 if self.availableEdit.currentText() == 'False' else 1

        self.cursor.execute(update_query, (title, author, category, available, int(pages), description, language,
                                           data[0][1],))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage("Book has been updated successfully!")

    def delete_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()
        book_title = self.title_search.text()
        delete_query = "DELETE FROM book WHERE title = %s"
        self.cursor.execute(delete_query, (book_title,))

        self.db.commit()
        self.db.close()
        self.statusBar().showMessage("The book has been deleted successfully!")

    #####################################################
    ############### user operations ######################

    def add_new_user(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        username = self.username.text()
        email = self.email.text()
        password = self.password.text()
        confirm_password = self.confirmPassword.text()

        user = self.cursor.execute('''
                       SELECT * FROM users WHERE username = (%s)
                       ''', (username,)).fetchone()

        if user:
            # open a dialog box to say that the username is already taken
            pass
        else:
            if username and email and password and confirm_password and password == confirm_password:
                self.cursor.execute('''
                            INSERT INTO users (username, password, email)
                            VALUES (%s, %s, %s)
                            ''', (username, password, email))
                self.db.commit()
                self.db.close()
                self.statusBar().showMessage("The user has been added successfully!")
            else:
                # Open the dialog box with the message
                print("Please don't create problem")

    # TODO Finish with the login functionality

    def show_emails(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='apartement')
        self.cursor = self.db.cursor()

        self.cursor.execute('''
          SELECT email FROM users
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
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        username = self.username2.text()
        password = self.password2.text()

        self.cursor.execute('''
                               SELECT * FROM users WHERE username = (%s) AND password= (%s)
                               ''', (username, password,))
        user = self.cursor.fetchone()
        #print(user)
        if user:
            change_visibility = [self.username3, self.password3, self.email2, self.confirmPassword2,
                                 self.saveChangesUser]

            for obj in change_visibility:
                obj.setEnabled(True)

            self.username3.setText(user[1])
            self.password3.setText(user[2])
            self.email2.setText(user[3])
            self.confirmPassword2.setText(user[2])
        else:
            print("Please don't create problem")

    def update_user(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        new_username = self.username3.text()
        new_email = self.email2.text()
        new_password = self.password3.text()
        new_confirm_password = self.confirmPassword2.text()

        username = self.username2.text()
        email = self.email.text()
        update_query = '''UPDATE users
                          SET username = %s , password= %s, email=%s
                          WHERE username = %s'''

        if new_username and new_email and new_password and new_confirm_password:
            self.cursor.execute(update_query, (new_username, new_password, new_email, username,))
            self.db.commit()
            self.db.close()
            change_visibility = [self.username3, self.password3, self.email2, self.confirmPassword2,
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
    login_=main_login()
    if login_:
        main()
    else:
        pass
# run this inside the terminal to avoid the error caused by the .qrc file :

# pyrcc5 icons.qrc -o icons_rc.py

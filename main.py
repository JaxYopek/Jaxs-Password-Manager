import sqlite3
import sys
import hashlib
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QLineEdit
import json
from password_manager_ui import Ui_MainWindow

db_file = "password_manager.db"
def connect():
    global connection, cursor
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
        ''')
    connection.commit()


# Hash master password
def hash_password(password):
   sha256 = hashlib.sha256()
   sha256.update(password.encode())
   return sha256.hexdigest()

def save_master_password(password):
    hashed_password = hash_password(password)
    with open('master_password.txt', 'w') as f:
        f.write(hashed_password)

def load_master_password():
    try:
        with open('master_password.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None



def generate_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)
    return key
def load_key():
    try:
        with open('key.key', 'rb') as key_file:
            return key_file.read()
    except FileNotFoundError:
        return generate_key()
class PasswordManager(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Password Manager")
        connect()

        # Connect buttons to respective functions
        self.ui.addpassword_button.clicked.connect(self.add_password)
        self.ui.getpassword_button.clicked.connect(self.get_password)
        self.ui.deletepassword_button.clicked.connect(self.delete_password)
        self.key = load_key()

        # Set or verify master password
        self.master_password_hash = load_master_password()
        if self.master_password_hash is None:
            self.set_master_password()
        else:
            self.verify_master_password()
        
    
    def set_master_password(self):
        master_password, ok = QInputDialog.getText(self, 'Set Master Password', 'Enter a new master password:', QLineEdit.Password)
        if ok and master_password:
            confirm_password, ok = QInputDialog.getText(self, 'Confirm Master Password', 'Confirm your master password:', QLineEdit.Password)
            if ok and confirm_password == master_password:
                save_master_password(master_password)
                QMessageBox.information(self, 'Success', 'Master password set successfully.')
            else:
                QMessageBox.warning(self, 'Error', 'Passwords do not match. Try again.')
                self.set_master_password()
        else:
            sys.exit()
    def verify_master_password(self):
        # Ask for master password until correct password is inputted
        while True:
            master_password, ok = QInputDialog.getText(self, 'Master Password', 'Enter your master password:', QLineEdit.Password)
            if not ok:
                sys.exit()
            if hash_password(master_password) == self.master_password_hash:
                break
            else:
                QMessageBox.warning(self, 'Error', 'Incorrect master password. Try again.')



    def generate_key(self):
        return Fernet.generate_key()

    def encrypt_password(self, password):
        return Fernet(self.key).encrypt(password.encode()).decode()
    
    def decrypt_password(self, encrypted_password):
        return Fernet(self.key).decrypt(encrypted_password.encode()).decode()

    def add_password(self):
            
        website = self.ui.website_entry.text()
        username = self.ui.username_entry.text()
        password = self.ui.password_entry.text()
        encrypted_password = self.encrypt_password(password)
        if not website or not username or not password:
            QMessageBox.warning(self,"Input Error", "All fields must be filled.")
            return


        cursor.execute('SELECT id FROM passwords WHERE website = ? AND username = ?', (website, username))
        result = cursor.fetchone()

        if result:
            # Update existing record
            cursor.execute('''
                UPDATE passwords 
                SET password = ? 
                WHERE website = ? AND username = ?
            ''', (encrypted_password, website, username))
            QMessageBox.information(self, "Success", "Password has been updated.")
            self.ui.username_entry.clear()
            self.ui.website_entry.clear()
            self.ui.password_entry.clear()
        else:
            # Insert new record
            cursor.execute('''
                INSERT INTO passwords (website, username, password) 
                VALUES (?, ?, ?)
            ''', (website, username, encrypted_password))
            QMessageBox.information(self, "Success", "Password added successfully.")
            self.ui.username_entry.clear()
            self.ui.website_entry.clear()
            self.ui.password_entry.clear()
        connection.commit()



        
    def get_password(self):
        website = self.ui.website_entry.text()
        username = self.ui.username_entry.text()

        if not website or not username:
            QMessageBox.warning(self,"Input Error", "Both website and username fields must be filled.")
            return
        
        cursor.execute('''
                        SELECT password 
                       FROM passwords 
                       WHERE username = ? AND
                       website = ?
                       ''', (username, website))
        result = cursor.fetchone()
        if result:
            encrypted_password = result[0]
            password = self.decrypt_password(encrypted_password)
            show_password(self, website, password)
            self.ui.username_entry.clear()
            self.ui.website_entry.clear()
        else:
            QMessageBox.warning(self, 'Error', "Website or username does not exist.")
            self.ui.username_entry.clear()
            self.ui.website_entry.clear()

    def delete_password(self):
        website = self.ui.website_entry.text()
        username = self.ui.username_entry.text()
        if not website or not username:
            QMessageBox.warning(self, "Input Error", "Both website and username fields must be filled.")
            return
        
        # Confirm password deletion with the user
        reply = QMessageBox.question(self, 'Confirmation', 
                                 f"Are you sure you want to delete the password for {username} at {website}?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            cursor.execute('''
                            DELETE FROM passwords 
                           WHERE website = ? AND username = ?
                           ''', (website, username))
            if cursor.rowcount == 0:
                QMessageBox.warning(self, "Error", "Website or username not found.")
                self.ui.username_entry.clear()
                self.ui.website_entry.clear()
                self.ui.password_entry.clear()
            else:
                QMessageBox.information(self, "Password Deleted", f'The password for {website} has been deleted successfully.')
                self.ui.username_entry.clear()
            self.ui.website_entry.clear()
            self.ui.password_entry.clear()
        else:
            QMessageBox.information(self, "Cancelled", "Password deletion has been cancelled.")
            
        connection.commit()

def show_password(self, website, password):
    # Create a custom QMessageBox
    msg_box = QMessageBox(self)
    msg_box.setWindowTitle("Password Retrieved!")
    msg_box.setText(f'The password to {website} is {password}.')

    # Add the standard information button
    msg_box.setStandardButtons(QMessageBox.Ok)

    # Add a custom button for "Copy to Clipboard"
    copy_button = msg_box.addButton("Copy to Clipboard", QMessageBox.ActionRole)

    # Show the message box
    msg_box.exec_()

    # Get the clicked button
    clicked_button = msg_box.clickedButton()

    if clicked_button == copy_button:
    # Copy the password to the clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(password)  # Copy password to clipboard
        print("Password copied to clipboard.")

            
if __name__ =='__main__':
    app = QApplication(sys.argv)
    ex = PasswordManager()
    ex.show()
    sys.exit(app.exec_())

        


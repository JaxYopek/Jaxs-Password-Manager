import sys
import hashlib
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QLineEdit
import json
from password_manager_ui import Ui_MainWindow



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
        self.setWindowTitle("Jax's Password Manager")

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
        try:
            with open('passwords.json', 'r') as file:
                data = json.load(file)
        except:
            data = []

        #Store password information in the form of a dictionary
        password_information = {'website': website,'username': username, 'password': encrypted_password}

        # Update password if website and username exist
        user_found = False
        for credential in data:
            if credential['website'] == website and credential['username'] == username:
                data.remove(credential)
                QMessageBox.information(self, "Success", "Password has been updated.")
                user_found = True
                break
        data.append(password_information)

        # Save updated password details to file
        with open('passwords.json','w') as file:
            json.dump(data,file, indent = 4)
        if not user_found:
            QMessageBox.information(self,"Success", "Password added successfully.")
        
    def get_password(self):
        website = self.ui.website_entry.text()
        username = self.ui.username_entry.text()

        if not website or not username:
            QMessageBox(self,"Input Error", "Both website and username fields must be filled.")
            return
        
        try:
            with open('passwords.json', 'r') as file:
                data = json.load(file)
        except:
            QMessageBox(self,"Error", "No existing password data.")
        

        # Retrieve password if the username and website exist
        user_found = False
        for credential in data:
            if credential['website'] == website and  credential['username'] == username:
                    encrypted_password = credential['password']
                    password = self.decrypt_password(encrypted_password)
                    QMessageBox.information(self, "Password Retrieved",f'The password to {username} at {website} is {password}.')
                    user_found = True
                    break
            if not user_found:
                 QMessageBox.warning(self, 'Error',"Website or username does not exist.")
            else:
                QMessageBox.warning(self,"Input Error", "All fields must be filled.")
            

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
            try:
                with open('passwords.json', 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                QMessageBox(self,"Error", "No existing password data.")
                return
            
            # If the website and username exist, remove the user credentials from the list
            user_found = False
            for credential in data:
                if credential['website'] == website and credential['username'] == username:
                    data.remove(credential)
                    user_found = True
                    break
            # Save updated password details to the file
            if user_found:
                with open('passwords.json', 'w') as file:
                    json.dump(data, file, indent=4)
                QMessageBox.information(self, "Success", f'Password for {username} at {website} has been deleted.')
            else:
                QMessageBox.warning(self, "Error", "Website or username not found.")
        else:
            QMessageBox.information(self, "Cancelled", "Password deletion has been cancelled.")


            
if __name__ =='__main__':
    app = QApplication(sys.argv)
    ex = PasswordManager()
    ex.show()
    sys.exit(app.exec_())

        


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        MainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.addpassword_button = QtWidgets.QPushButton(self.centralwidget)
        self.addpassword_button.setGeometry(QtCore.QRect(150, 410, 141, 32))
        self.addpassword_button.setObjectName("addpassword_button")
        self.getpassword_button = QtWidgets.QPushButton(self.centralwidget)
        self.getpassword_button.setGeometry(QtCore.QRect(150, 450, 141, 32))
        self.getpassword_button.setObjectName("getpassword_button")
        self.website_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.website_entry.setGeometry(QtCore.QRect(300, 270, 221, 21))
        self.website_entry.setObjectName("website_entry")
        self.username_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.username_entry.setGeometry(QtCore.QRect(300, 320, 221, 21))
        self.username_entry.setObjectName("username_entry")
        self.password_entry = QtWidgets.QLineEdit(self.centralwidget)
        self.password_entry.setGeometry(QtCore.QRect(300, 370, 221, 21))
        self.password_entry.setObjectName("password_entry")
        self.website = QtWidgets.QLabel(self.centralwidget)
        self.website.setGeometry(QtCore.QRect(160, 270, 71, 16))
        self.website.setObjectName("website")
        self.username = QtWidgets.QLabel(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(160, 320, 91, 20))
        self.username.setObjectName("username")
        self.password = QtWidgets.QLabel(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(160, 370, 61, 20))
        self.password.setObjectName("password")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(150, 70, 451, 131))
        font = QtGui.QFont()
        font.setFamily("Futura")
        font.setPointSize(40)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.deletepassword_button = QtWidgets.QPushButton(self.centralwidget)
        self.deletepassword_button.setGeometry(QtCore.QRect(500, 430, 131, 41))
        self.deletepassword_button.setStyleSheet("QPushButton{\n"
"color: rgb(255,0,0);\n"
"background: transparent;\n"
"border: none;\n"
"}")
        self.deletepassword_button.setText("")
        icon = QtGui.QIcon.fromTheme("trash")
        if icon.isNull():
            icon = QtGui.QIcon("trash_icon.png")
        self.deletepassword_button.setIcon(icon)
        self.deletepassword_button.setIconSize(QtCore.QSize(20, 25))
        self.deletepassword_button.setAutoDefault(True)
        self.deletepassword_button.setObjectName("deletepassword_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 36))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addpassword_button.setText(_translate("MainWindow", "Add New Password"))
        self.getpassword_button.setText(_translate("MainWindow", "Get Password"))
        self.website.setText(_translate("MainWindow", "Website:"))
        self.username.setText(_translate("MainWindow", "Username:"))
        self.password.setText(_translate("MainWindow", "Password:"))
        self.label_4.setText(_translate("MainWindow", "Jax\'s Password Manager"))
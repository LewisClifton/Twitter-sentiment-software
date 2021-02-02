from database import Database
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, \
    QMainWindow, QAction, QWidget, QTabWidget, QLabel, QGroupBox, QScrollArea, QGridLayout, QMessageBox, QInputDialog
from PyQt5 import Qt
from PyQt5.QtCore import Qt
import time


def get_screen_size():
    sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
    return sizeObject.width(), sizeObject.height()


class MainWindow(QMainWindow):
    def __init__(self, parent):
        super(MainWindow, self).__init__()
        self.parent = parent

    def initUI(self):  # Initialise the UI
        self.setWindowTitle('Sentiment Analysis')

        # Establish geometry
        width = 1200
        height = int(width * 2 / 3)

        # Centre the window
        self.setGeometry(get_screen_size()[0] / 2 - width / 2, get_screen_size()[1] / 2 - height / 2, 0, 0)

        # Set fixed dimensions for the window so the user can't accidentally change the window size
        self.setFixedSize(width, height)

        # Add menu
        self.add_menu()

        # Add Tabs
        self.tab_widget = TabHandler(self)
        self.setCentralWidget(self.tab_widget)

        self.show()  # Shows the main window on the screen

    def add_menu(self):  # Add the menu to the window
        # ADD MENU
        mainMenu = self.menuBar()  # Gives the window a menu bar

        # File:
        fileMenu = mainMenu.addMenu('File')  # Add file menu
        newButton = QAction('New', self)
        newButton.triggered.connect(self.new)
        fileMenu.addAction(newButton)
        saveButton = QAction('Save', self)
        fileMenu.addAction(saveButton)
        printButton = QAction('Print', self)
        fileMenu.addAction(printButton)
        logoutButton = QAction('Logout', self)
        logoutButton.triggered.connect(self.sign_out)
        fileMenu.addAction(logoutButton)
        exitButton = QAction('Exit', self)
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # Preferences:
        prefMenu = mainMenu.addMenu('Preferences')  # Add preferences menu
        # colButton = QAction('Colour Scheme', self)
        # colButton.triggered.connect(self.click)
        #prefMenu.addAction(colButton)

        # Settings:
        setMenu = mainMenu.addMenu('Settings')  # Add settings menu
        companyButton = QAction('Company', self)
        setMenu.addAction(companyButton)

        # Account:
        accMenu = mainMenu.addMenu('Account')  # Add account menu
        passButton = QAction('Change Password', self)
        accMenu.addAction(passButton)

        # Help:
        helpMenu = mainMenu.addMenu('Help')  # Add help menu
        guideButton = QAction('User Guide', self)
        helpMenu.addAction(guideButton)
        aboutButton = QAction('About', self)
        aboutButton.triggered.connect(self.about)
        helpMenu.addAction(aboutButton)

    def change_company(self):
        company, text_entered = QInputDialog.getText(self, 'Change company', 'Enter company name:')
        if text_entered:
            pass

    def user_guide(self):
        pass

    def about(self):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Twitter Sentiment Analysis")
        msg.setInformativeText("Created by Lewis Clifton")
        msg.setWindowTitle("About")


        retval = msg.exec_()

    def sign_out(self):
        self.close()

        time.sleep(0.25)

        self.parent.widget.show()
        self.parent.username = None

        self.parent.login.username.setText("")
        self.parent.login.password.setText("")
        self.parent.signup.username.setText("")
        self.parent.signup.password.setText("")
        self.parent.signup.company.setText("")

    def new(self):
        topic, text_entered = QInputDialog.getText(self, 'New topic', 'Enter topic name:')
        if text_entered:
            pass

    def change_theme(self):
        self.palette_index = 0

        self.palette_colours = [
            [0, 0, 128],
            [62, 80, 91]
        ]

        self.palette = self.palette()
        self.setPalette(self.palette)

        self.palette_index += 1
        if self.palette_index > len(self.palette_colours):
            self.palette_index = 0
        self.palette.setColor(QPalette.Button, QColor(self.palette_colours[self.palette_index][0],
                                                      self.palette_colours[self.palette_index][1],
                                                      self.palette_colours[self.palette_index][2]))

        self.setPalette(self.palette)


class TabHandler(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        # Create a layout to put all of the tabs on
        self.tabLayout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)

        # Add the dashboard
        dashboard = Dashboard()
        self.tabs.addTab(dashboard, "Dashboard")

        # Add a tab
        # for i in range(10):
        self.add_tab()

        # Add all of the tabs to the tab layout
        self.tabLayout.addWidget(self.tabs)

        # Place the tab layout on the window
        self.setLayout(self.tabLayout)

    def add_tab(self):  # Add a tab
        tabName = "newtab"
        # Create the new tab
        newTab = TopicTab(tabName)
        self.tabs.addTab(newTab, tabName)


class Tab(QWidget):
    def __init__(self):
        super(Tab, self).__init__()

    def initUI(self):
        self.windowLayout = QVBoxLayout()

        # TOP LAYOUT:
        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(QLabel(self.name))
        self.topLayout.addWidget(QLabel("Average Sentiment: 4"))
        self.topLayout.addWidget(QLabel("500 tweets"))
        self.topLayout.addWidget(QLabel("500 unique authors"))

        # BOTTOM LAYOUT:
        # scroll box:
        self.bottomLayout = QHBoxLayout()
        formLayout = QFormLayout()
        groupBox = QGroupBox("Tweets")
        usernames = ["Username" for i in range(25)]
        tweets = [QLabel("Content") for i in range(25)]
        for i in range(25):
            formLayout.addRow(usernames[i], tweets[i])
        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(400)
        scroll.setFixedHeight(400)
        self.bottomLayout.addWidget(scroll)

        # grid layout:
        self.horizontalGroupBox = QGroupBox()
        self.gridLayout = QGridLayout()
        # self.gridLayout.setColumnStretch(0, 4)

        self.gridLayout.addWidget(QPushButton('1'), 0, 0)
        self.gridLayout.addWidget(QPushButton('2'), 0, 1)
        self.gridLayout.addWidget(QPushButton('3'), 1, 0)
        self.gridLayout.addWidget(QPushButton('4'), 1, 1)

        self.horizontalGroupBox.setLayout(self.gridLayout)
        self.bottomLayout.addWidget(self.horizontalGroupBox)

        self.windowLayout.addLayout(self.topLayout)
        self.windowLayout.addLayout(self.bottomLayout)

        self.setLayout(self.windowLayout)


class Dashboard(Tab):
    def __init__(self):
        super(Dashboard, self).__init__()
        self.name = "Company name"
        self.initUI()


class TopicTab(Tab):
    def __init__(self, name):
        super(TopicTab, self).__init__()
        self.name = name
        self.initUI()


class Login(QDialog):  # Inherits QDialog so the window can be put on the stack widget
    def __init__(self, parent):  # The parent parameter is the stack widget
        super(Login, self).__init__()
        self.parent = parent  # Gives the login instance access to change the stack widget

    def initUI(self):  # Initialise the UI
        # Change the window title
        self.parent.widget.setWindowTitle("Login")

        # Establish geometry and centre the window
        width = 400
        height = int(width * 3 / 4)
        self.parent.widget.setGeometry(get_screen_size()[0] / 2 - width / 2, get_screen_size()[1] / 2 - height / 2, 0,
                                       0)

        # Set fixed dimensions for the window so the user can't accidentally change the window size
        self.parent.widget.setFixedSize(width, height)

        # Create layout for the window
        windowLayout = QVBoxLayout()
        windowLayout.setAlignment(Qt.AlignCenter)

        # Create layouts to go on the window:
        # Tile Layout
        titleLayout = QHBoxLayout()
        titleLayout.setAlignment(Qt.AlignHCenter)
        title = QtWidgets.QLabel("Twitter Sentiment Analysis")
        title.setFont(QFont("Arial", 20))
        titleLayout.addWidget(title)

        prompt = QtWidgets.QLabel("Please login or sign up to continue")
        prompt.setFont(QFont("Arial", 10))

        # Fields layout
        fieldsLayout = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        fieldsLayout.addRow("Username", self.username)
        fieldsLayout.addRow("Password", self.password)

        # Error message layout
        self.errorMsg = QLabel("Incorrect Username or password")
        self.errorMsg.setAlignment(Qt.AlignCenter)
        self.errorMsg.setStyleSheet('color: red')
        self.errorMsg.hide()

        # Button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignCenter)

        loginButton = QPushButton("Login")
        loginButton.setFixedWidth(100)
        loginButton.clicked.connect(self.login)

        signupButton = QPushButton("Sign Up")
        signupButton.setFixedWidth(100)
        signupButton.clicked.connect(self.signUp)

        buttonLayout.addWidget(loginButton)
        buttonLayout.addSpacing(50)
        buttonLayout.addWidget(signupButton)

        # Add to elements layout
        windowLayout.addLayout(titleLayout)
        windowLayout.addSpacing(20)
        windowLayout.addWidget(prompt)
        windowLayout.addSpacing(5)
        windowLayout.addLayout(fieldsLayout)
        windowLayout.addSpacing(5)
        windowLayout.addWidget(self.errorMsg)
        windowLayout.addSpacing(10)
        windowLayout.addLayout(buttonLayout)

        # Set the window's main layout
        self.setLayout(windowLayout)

    def login(self):

        # Get the entered login details
        entered_username = self.username.text()
        entered_password = self.password.text()

        # Check database to see if login details are valid
        credentials_valid = Database.authenticate(entered_username, entered_password)

        if credentials_valid:
            # Run the controller function which shows the main window
            self.parent.show_main_window(self.username.text())
        else:
            # Show the error message
            self.errorMsg.show()

    def signUp(self):
        # Show the sign up screen
        self.parent.show_sign_up()


class SignUp(QDialog):
    def __init__(self, parent):
        super(SignUp, self).__init__()
        self.parent = parent

    def initUI(self):  # Initialise the UI
        # Change the window title
        self.parent.widget.setWindowTitle("Sign Up")

        # Establish geometry
        width = 400
        height = int(width * 3 / 4)

        # Change the width of the controller widget to be the size of the sign up screen
        self.parent.widget.setGeometry(get_screen_size()[0] / 2 - width / 2, get_screen_size()[1] / 2 - height / 2, 0,
                                       0)

        # Set fixed dimensions for the window so the user can't accidentally change the window size
        self.parent.widget.setFixedSize(width, height)

        # Create layout for the window
        windowLayout = QVBoxLayout()
        windowLayout.setAlignment(Qt.AlignCenter)

        # Create layouts to go on the window:
        # Tile Layout
        titleLayout = QHBoxLayout()
        titleLayout.setAlignment(Qt.AlignHCenter)
        title = QtWidgets.QLabel("Register")
        title.setFont(QFont("Arial", 20))
        titleLayout.addWidget(title)

        prompt = QtWidgets.QLabel("Please sign up to continue")
        prompt.setFont(QFont("Arial", 10))

        # Fields layout
        fieldsLayout = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.company = QLineEdit()
        fieldsLayout.addRow("Username", self.username)
        fieldsLayout.addRow("Password", self.password)
        fieldsLayout.addRow("Company Name", self.company)

        # Creating the error message widget
        self.errorMsg = QLabel(self)
        self.errorMsg.setAlignment(Qt.AlignCenter)
        self.errorMsg.setStyleSheet('color: red')
        self.errorMsg.hide()

        # Button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignHCenter)

        signupButton = QPushButton("Sign Up")
        signupButton.setFixedWidth(100)
        signupButton.clicked.connect(self.signUp)

        loginButton = QPushButton("Back to login")
        loginButton.setFixedWidth(100)
        loginButton.clicked.connect(self.login)

        buttonLayout.addWidget(loginButton)
        buttonLayout.addSpacing(50)
        buttonLayout.addWidget(signupButton)

        # Add to elements layout
        windowLayout.addLayout(titleLayout)
        windowLayout.addSpacing(20)
        windowLayout.addWidget(prompt)
        windowLayout.addSpacing(5)
        windowLayout.addLayout(fieldsLayout)
        windowLayout.addSpacing(5)
        windowLayout.addWidget(self.errorMsg)
        windowLayout.addSpacing(10)
        windowLayout.addLayout(buttonLayout)

        # Set the window's main layout
        self.setLayout(windowLayout)

    def signUp(self):
        # Get the entered details
        entered_username = self.username.text()
        entered_password = self.password.text()
        entered_company = self.company.text()

        # Check if details valid and if they are, add to database
        error = Database.new_user(entered_username, entered_password, entered_company)

        if error:
            # Show the relevant error message provided by the "new_user" function
            self.errorMsg.setText(error)
            self.errorMsg.show()
        else:
            # Run the controller function which shows the main window
            self.parent.show_main_window(self.username.text())


    def login(self):
        # Go back to the login screen
        self.parent.show_login()

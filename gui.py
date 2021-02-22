import time
import main

from PyQt5 import QtWidgets

# USER INTERFACE
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, \
    QFormLayout, QWidget, QTabWidget, QLabel, QListView, QGridLayout, QGroupBox, QScrollArea, QMenu, QAction, QMenuBar
from PyQt5 import Qt
from PyQt5.QtCore import Qt


def get_screen_size():
    sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
    return (sizeObject.width(), sizeObject.height())


class MainWindow(QMainWindow):
    def __init__(self, parent):
        super(MainWindow, self).__init__()
        self.parent = parent

    def initUI(self):
        self.setWindowTitle('Sentiment Analysis')

        # Establish geometry
        width = 1200
        height = int(width * 2 / 3)
        fontSize = int(width / 40)

        self.setGeometry(get_screen_size()[0] / 2 - width / 2, get_screen_size()[1] / 2 - height / 2, 0, 0)
        self.setFixedSize(width, height)

        self.windowLayout = QVBoxLayout()

        self.tab_widget = MyTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.add_menu()

        self.show()

    def add_menu(self):  # Add the menu to the window
        # ADD MENU
        mainMenu = self.menuBar()  # Gives the window a menu bar

        # File:
        fileMenu = mainMenu.addMenu('File')  # Add file menu
        newButton = QAction('New', self)
        fileMenu.addAction(newButton)
        saveButton = QAction('Save', self)
        fileMenu.addAction(saveButton)
        printButton = QAction('Print', self)
        fileMenu.addAction(printButton)
        logoutButton = QAction('Logout', self)
        fileMenu.addAction(logoutButton)
        exitButton = QAction('Exit', self)
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # Preferences:
        prefMenu = mainMenu.addMenu('Preferences')  # Add preferences menu
        colButton = QAction('Colour Scheme', self)
        prefMenu.addAction(colButton)

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
        helpMenu.addAction(aboutButton)

    def signOut(self):
        self.close()
        time.sleep(0.5)
        self.parent.login.clear()
        self.parent.show_login()
        self.parent.widget.show()


class MyTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)

        dashboard = Dashboard()
        self.tabs.addTab(dashboard, "Dashboard")
        self.layout.addWidget(self.tabs)

        # self.add_tab()

        self.setLayout(self.layout)

    def add_tab(self):
        # Add tabs
        tab = Topic("newtab")
        self.tabs.addTab(tab, tab.name)
        tab.initUI()
        # Add tabs to widget
        self.layout.addWidget(self.tabs)


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
        super().__init__()
        self.name = "Google"
        self.initUI()


#
class Topic(Tab):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.initUI()


class Login(QDialog):
    def __init__(self, parent):
        super(Login, self).__init__()
        self.parent = parent

    def initUI(self):
        self.parent.widget.setWindowTitle("Login")

        # Establish geometry
        width = 400
        height = int(width * 3 / 4)

        self.parent.widget.setGeometry(get_screen_size()[0] / 2 - width / 2, get_screen_size()[1] / 2 - height / 2, 0,
                                       0)
        self.parent.widget.setFixedSize(width, height)

        # Create layout for the window
        windowLayout = QVBoxLayout()
        windowLayout.setAlignment(Qt.AlignCenter)

        # Create layouts to go on the window:
        ## Tile Layout
        titleLayout = QHBoxLayout()
        titleLayout.setAlignment(Qt.AlignHCenter)
        title = QtWidgets.QLabel("Twitter Sentiment Analysis")
        title.setFont(QFont("Arial", 20))
        titleLayout.addWidget(title)

        prompt = QtWidgets.QLabel("Please login or sign up to continue")
        prompt.setFont(QFont("Arial", 10))

        ## Fields layout
        fieldsLayout = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        fieldsLayout.addRow("Username", self.username)
        fieldsLayout.addRow("Password", self.password)

        ## Button layout
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
        windowLayout.addSpacing(20)
        windowLayout.addLayout(buttonLayout)

        # Set the window's main layout
        self.setLayout(windowLayout)

    def login(self):
        print("logged in")
        # username = self.username.text()
        # password = self.password.text()
        # print(main.db.authenticate(username, password))
        # self.parent.show_main_window()

    def signUp(self):
        self.parent.show_sign_up()

    def clear(self):
        self.username.clear()
        self.password.clear()


class SignUp(QDialog):
    def __init__(self, parent):
        super(SignUp, self).__init__()
        self.parent = parent

    def initUI(self):
        self.parent.widget.setWindowTitle("Sign Up")

        # Create layout for the window
        windowLayout = QVBoxLayout()
        windowLayout.setAlignment(Qt.AlignCenter)

        # Create layouts to go on the window:
        ## Tile Layout
        titleLayout = QHBoxLayout()
        titleLayout.setAlignment(Qt.AlignHCenter)
        title = QtWidgets.QLabel("Sign Up")
        title.setFont(QFont("Arial", 20))
        titleLayout.addWidget(title)

        ## Fields layout
        fieldsLayout = QFormLayout()
        fieldsLayout.addRow("Username", QLineEdit())
        fieldsLayout.addRow("Password", QLineEdit())
        fieldsLayout.addRow("Company Name", QLineEdit())

        ## Button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignHCenter)

        loginButton = QPushButton("Sign Up")
        loginButton.setFixedWidth(100)
        loginButton.clicked.connect(self.signUp)

        buttonLayout.addWidget(loginButton)

        # Add to elements layout
        windowLayout.addLayout(titleLayout)
        windowLayout.addSpacing(20)
        windowLayout.addLayout(fieldsLayout)
        windowLayout.addSpacing(20)
        windowLayout.addLayout(buttonLayout)

        # Set the window's main layout
        self.setLayout(windowLayout)

    def signUp(self):
        self.parent.show_main()

    def login(self):
        self.parent.show_login()


class Controller:
    def __init__(self):
        super().__init__()

        self.widget = QtWidgets.QStackedWidget()

        self.login = Login(self)
        self.widget.addWidget(self.login)

        self.signup = SignUp(self)
        self.widget.addWidget(self.signup)

        self.show_login()

    def show_login(self):
        self.login.initUI()
        self.widget.setCurrentIndex(0)
        self.widget.show()

    def show_sign_up(self):
        self.signup.initUI()
        self.widget.setCurrentIndex(1)
        self.widget.show()

    def show_main(self):
        self.widget.hide()
        self.mainWindow = MainWindow(self)
        self.mainWindow.initUI()

# def get_screen_size():
#     sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
#     return (sizeObject.width(), sizeObject.height())
#
# class MainWindow(QMainWindow):
#     def __init__(self, parent):
#         super(MainWindow, self).__init__()
#         self.parent = parent
#
#     def initUI(self):
#         self.parent.setWindowTitle('Sentiment Analysis')
#
#         # Establish geometry
#         width = 1200
#         height = int(width * 2 / 3)
#         fontSize = int(width / 40)
#
#         self.parent.setGeometry(get_screen_size()[0] / 2 - width / 2, get_screen_size()[1] / 2 - height / 2, 0,
#                                        0)
#         self.parent.setFixedSize(width, height)
#
#         # Create layout for the window
#         #windowLayout = QVBoxLayout()
#         # windowLayout.setAlignment(Qt.AlignCenter)
#
#         # Add menu
#         # menubar = self.parent.menuBar()
#         # fileMenu = menubar.addMenu('File')
#         # fileMenu = menubar.addMenu('Preference')
#         # fileMenu = menubar.addMenu('Settings')
#         # fileMenu = menubar.addMenu('Account')
#         # fileMenu = menubar.addMenu('Help')
#
#
#         # Add tabs
#
#         self.tab_widget = MyTabWidget(self.parent)
#         self.parent.setCentralWidget(self.tab_widget)
#
#         self.parent.show()
#
# class MyTabWidget(QWidget):
#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)
#         self.layout = QVBoxLayout(self)
#
#         # Initialize tab screen
#         self.tabs = QTabWidget()
#         self.tab1 = QWidget()
#         self.tab2 = QWidget()
#         self.tab3 = QWidget()
#         self.tabs.resize(300, 200)
#
#         # Add tabs
#         self.tabs.addTab(self.tab1, "Geeks")
#         self.tabs.addTab(self.tab2, "For")
#         self.tabs.addTab(self.tab3, "Geeks")
#
#         # Create first tab
#         self.tab1.layout = QVBoxLayout(self)
#         self.l = QLabel()
#         self.l.setText("This is the first tab")
#         self.tab1.layout.addWidget(self.l)
#         self.tab1.setLayout(self.tab1.layout)
#
#             # def add_tab(self, name):
#     #     tab = Tab()
#     #     self.tabs.addTab(tab, name)
#
#
#
# class Login(QDialog):
#     def __init__(self, parent):
#         super(Login, self).__init__()
#         self.parent = parent
#
#     def initUI(self):
#         self.parent.widget.setWindowTitle("Login")
#
#         # Establish geometry
#         width = 400
#         height = int(width * 3 / 4)
#
#         self.parent.widget.setGeometry(get_screen_size()[0] / 2 - width / 2, get_screen_size()[1] / 2 - height / 2, 0,
#                                        0)
#         self.parent.widget.setFixedSize(width, height)
#
#         # Create layout for the window
#         windowLayout = QVBoxLayout()
#         windowLayout.setAlignment(Qt.AlignCenter)
#
#         # Create layouts to go on the window:
#         ## Tile Layout
#         titleLayout = QHBoxLayout()
#         titleLayout.setAlignment(Qt.AlignHCenter)
#         title = QtWidgets.QLabel("Twitter Sentiment Analysis")
#         title.setFont(QFont("Arial", 20))
#         titleLayout.addWidget(title)
#
#         prompt = QtWidgets.QLabel("Please login or sign up to continue")
#         prompt.setFont(QFont("Arial", 10))
#
#         ## Fields layout
#         fieldsLayout = QFormLayout()
#         fieldsLayout.addRow("Username", QLineEdit())
#         fieldsLayout.addRow("Password", QLineEdit())
#
#         ## Button layout
#         buttonLayout = QHBoxLayout()
#         buttonLayout.setAlignment(Qt.AlignCenter)
#
#         loginButton = QPushButton("Login")
#         loginButton.setFixedWidth(100)
#         loginButton.clicked.connect(self.login)
#
#         signupButton = QPushButton("Sign Up")
#         signupButton.setFixedWidth(100)
#         signupButton.clicked.connect(self.signUp)
#
#         buttonLayout.addWidget(loginButton)
#         buttonLayout.addSpacing(50)
#         buttonLayout.addWidget(signupButton)
#
#         # Add to elements layout
#         windowLayout.addLayout(titleLayout)
#         windowLayout.addSpacing(20)
#         windowLayout.addWidget(prompt)
#         windowLayout.addSpacing(5)
#         windowLayout.addLayout(fieldsLayout)
#         windowLayout.addSpacing(20)
#         windowLayout.addLayout(buttonLayout)
#
#         # Set the window's main layout
#         self.setLayout(windowLayout)
#
#
#
#     def login(self):
#         print("logged in")
#         self.parent.show_main()
#
#     def signUp(self):
#         self.parent.show_sign_up()
#
#
# class SignUp(QDialog):
#     def __init__(self, parent):
#         super(SignUp, self).__init__()
#         self.parent = parent
#
#     def initUI(self):
#         self.parent.widget.setWindowTitle("Sign Up")
#
#         # Create layout for the window
#         windowLayout = QVBoxLayout()
#         windowLayout.setAlignment(Qt.AlignCenter)
#
#         # Create layouts to go on the window:
#         ## Tile Layout
#         titleLayout = QHBoxLayout()
#         titleLayout.setAlignment(Qt.AlignHCenter)
#         title = QtWidgets.QLabel("Sign Up")
#         title.setFont(QFont("Arial", 20))
#         titleLayout.addWidget(title)
#
#         ## Fields layout
#         fieldsLayout = QFormLayout()
#         fieldsLayout.addRow("Username", QLineEdit())
#         fieldsLayout.addRow("Password", QLineEdit())
#         fieldsLayout.addRow("Company Name", QLineEdit())
#
#         ## Button layout
#         buttonLayout = QHBoxLayout()
#         buttonLayout.setAlignment(Qt.AlignHCenter)
#
#         loginButton = QPushButton("Sign Up")
#         loginButton.setFixedWidth(100)
#         loginButton.clicked.connect(self.signUp)
#
#         buttonLayout.addWidget(loginButton)
#
#         # Add to elements layout
#         windowLayout.addLayout(titleLayout)
#         windowLayout.addSpacing(20)
#         windowLayout.addLayout(fieldsLayout)
#         windowLayout.addSpacing(20)
#         windowLayout.addLayout(buttonLayout)
#
#         # Set the window's main layout
#         self.setLayout(windowLayout)
#
#     def signUp(self):
#         self.parent.show_main()
#
#     def login(self):
#         self.parent.show_login()
#
#
# class Controller():
#     def __init__(self):
#         super().__init__()
#
#         self.widget = QtWidgets.QStackedWidget()
#
#         self.login = Login(self)
#         self.widget.addWidget(self.login)
#
#         self.signup = SignUp(self)
#         self.widget.addWidget(self.signup)
#
#         self.show_login()
#
#     def show_login(self):
#         self.login.initUI()
#         self.widget.setCurrentIndex(0)
#         self.widget.show()
#
#     def show_sign_up(self):
#         self.signup.initUI()
#         self.widget.setCurrentIndex(1)
#         self.widget.show()
#
#     def show_main(self):
#         self.widget = None
#         self.mainWindow = MainWindow(self)
#         self.mainWindow.initUI()
#
#
#
# def gui():
#     app = QApplication(sys.argv)
#     userInterface = Controller()
#
#     app.exec_()

from PyQt5.QtWidgets import QApplication
# from PyQt5.uic.properties import QtWidgets
from PyQt5 import QtWidgets
from concurrent.futures import ThreadPoolExecutor

import new_gui as gui
from database import *
import sys
from model import Model


class Controller:
    def __init__(self):
        # Create the window stack
        self.widget = QtWidgets.QStackedWidget()

        # Create the login and signup windows and add them to the widget stack
        self.login = gui.Login(self)
        self.login.initUI()
        self.widget.addWidget(self.login)

        self.signup = gui.SignUp(self)
        self.signup.initUI()
        self.widget.addWidget(self.signup)

        # Show the current window
        self.widget.show()

    def show_main_window(self, username):
        # Hide the login and sign up window stack
        self.widget.hide()

        # Begin the main function
        self.main(username)

    def show_sign_up(self):
        # Change the window title
        self.widget.setWindowTitle("Sign Up")

        # Change stack index to show the sign up screen
        self.widget.setCurrentIndex(1)

    def show_login(self):
        # Change the window title
        self.widget.setWindowTitle("Login")

        # Sets the index of the stack so the login screen is shown
        self.widget.setCurrentIndex(0)

    def main(self, username):

        # Instantiate the user class
        self.user = User(username)

        # Sets up the user interface elements of the main window
        self.mainWindow = gui.MainWindow(self, self.user)
        self.mainWindow.initUI()




def main():
    app = QApplication(sys.argv)  # Starts the application
    app.setStyle('Fusion') # Set the colour theme of the windows
    userInterface = Controller()  # Create an instance of the controller
    app.exec_()  # Creates a loop, displaying the application gui until it is exited


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor: # Create thread pool
        executor.submit(Model.load_model) # Creates a thread to load the model
        executor.submit(main) # Create another thread that runs the application




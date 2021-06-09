# Make necessary imports
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from concurrent.futures import ThreadPoolExecutor
import sys

# Import other files
from model import Model
import gui
from data_handling import *


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

        # Show the login screen
        self.show_login()
        self.widget.show()

    def show_main_window(self, username):
        # Hide the login and sign up window stack
        self.widget.hide()

        # Begin the main function
        self.main(username)

    def main(self, username):

        # Instantiate the user class
        self.user = User(username)

        # Sets up the user interface elements of the main window
        self.mainWindow = gui.MainWindow(self, self.user)
        self.mainWindow.initUI()

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



def main():
    # Create the application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    userInterface = Controller()  # Create an instance of the controller

    # Creates a main loop for the application so it stays open
    app.exec_()

if __name__ == "__main__":
    # Use threading to load the model and run the rest of the application at the same time
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(Model.load_model) # Creates a thread to load the model
        executor.submit(main) # Create another thread that runs the application




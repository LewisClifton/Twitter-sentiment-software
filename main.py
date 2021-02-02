from PyQt5.QtWidgets import QApplication
# from PyQt5.uic.properties import QtWidgets
from PyQt5 import QtWidgets

import new_gui as gui
from database import *
import sys

class User:
    def __init__(self, username, id=None, company=None):
        self.id = id
        self.username = username
        self.company = company
        self.topics = []


    def new_topic(self, topic):
        Database.new_topic(self.id, topic)

    def get_topics(self):
        for topic in Database.get_user_topics(self.id):
            self.topics.append(topic)
#
#
# class Topic:
#     def __init__(self, name):
#         self.name = name
#         self.num_of_tweets = None
#         self.predictions = None
#         self.sentiments = None
#         self.tweets = None
#         self.likes = None
#
#     def get_tweets(self):
#         self.tweets = scraper.Scraper.get_tweets(self.name)
#
#         self.tweets = [tweet[0] for tweet in self.tweets]
#         self.likes = [tweet[1] for tweet in self.tweets]
#
#     def get_predictions(self):
#         self.predictions = model.Model.make_tweet_predictions(self.tweets)
#
#         self.sentiments = ["Positive" if pred == 0 else "Negative" for pred in self.predictions]

class Controller:  # Controls what happens during the running of the program
    def __init__(self):
        self.widget = QtWidgets.QStackedWidget()  # Create the window stack

        self.login = gui.Login(self)  # Instantiates the login screen
        self.login.initUI()
        self.widget.addWidget(self.login)  # Adds the login to the stack

        self.signup = gui.SignUp(self)
        self.signup.initUI()
        self.widget.addWidget(self.signup)

        self.mainWindow = gui.MainWindow(self)  # Instantiates the main window (don't need to add to the stack)

        self.show_login()  # Runs the "show_sign_up" method, showing the sign up form
        self.widget.show()  # Shows the current window on the stack

        self.user = None

    def show_main_window(self, username):  # Is run to show the main window

        self.widget.hide()  # Hide the login and sign up window stack
        self.mainWindow.initUI()  # Sets up the user interface elements of the main window

        self.main(username)


    def show_sign_up(self):  # Is run to show the signing up screen
        self.widget.setCurrentIndex(1)  # Sets the index of the stack so the sign up screen is shown

    def show_login(self):  # Is run to show the login screen
        self.widget.setCurrentIndex(0)  # Sets the index of the stack so the login screen is shown

    def main(self, username):

        user_id, company = Database.get_user_info(username)

        self.user = User(username, user_id, company)
       #  user.new_topic("Dogs")
        user.get_topics()
        print(user.topics)





def main():
    app = QApplication(sys.argv)  # Starts the application
    app.setStyle('Fusion')
    userInterface = Controller()  # Create an instance of the controller
    app.exec_()  # Creates a loop, displaying the application gui until it is exited


main()

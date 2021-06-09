# Make necessary UI imports
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPainter, QPen
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QMainWindow, QAction, QWidget, \
    QTabWidget, QLabel, QGroupBox, QScrollArea, QGridLayout, QMessageBox, QInputDialog, QDialog, QPushButton, QSlider
from PyQt5 import Qt
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice, QBarCategoryAxis, QBarSet, QLineSeries, \
    QValueAxis, QBarSeries
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from wordcloud import WordCloud

# Import other files
from database import Database
from data_handling import *
import time
import os
import math
from datetime import datetime


def get_screen_size():
    sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
    return sizeObject.width(), sizeObject.height()


class MainWindow(QMainWindow):
    def __init__(self, parent, user):
        super(MainWindow, self).__init__()
        self.parent = parent

        self.user = user

    def initUI(self):  # Initialise the UI
        # self.setStyleSheet("QLabel{font-size: 18pt;}, QButton.text{font-size: 18pt;}")

        self.setWindowTitle('Sentiment Analysis')

        # Establish geometry
        width = 1500
        height = int(width * 9 / 16)

        # Centre the window
        self.setGeometry(get_screen_size()[0] / 2 - width / 2, get_screen_size()[1] / 2 - height / 2, width, height)

        # Maximise the window
        self.showMaximized()

        # Add menu
        self.add_menu()

        # Add Tabs
        self.tab_widget = TabHandler(self)
        self.setCentralWidget(self.tab_widget)

        # Create a tab manager instance
        self.TopicManagerPopUp = TopicManagerPopUp(self)
        self.TopicManagerPopUp.hide()

        # Create a password changer instance
        self.PasswordManagerPopUp = PasswordPopUp(self)
        self.PasswordManagerPopUp.hide()

        # Create a company changer instance
        self.CompanyManagerPopUp = CompanyPopUp(self)
        self.CompanyManagerPopUp.hide()

        # Check internet connection
        self.check_connection()

        self.palette = self.palette()
        self.setPalette(self.palette)

        self.show()  # Shows the main window on the screen

    def add_menu(self):
        # Add the menu bar to the window?
        mainMenu = self.menuBar()

        # File:
        fileMenu = mainMenu.addMenu('File')
        saveButton = QAction('Save', self)
        saveButton.triggered.connect(self.save)
        fileMenu.addAction(saveButton)
        logoutButton = QAction('Logout', self)
        logoutButton.triggered.connect(self.sign_out)
        fileMenu.addAction(logoutButton)
        exitButton = QAction('Exit', self)
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # Settings:
        setMenu = mainMenu.addMenu('Settings')  # Add settings menu
        companyButton = QAction('Change Company', self)
        companyButton.triggered.connect(self.change_company)
        manageTopicsButton = QAction('Topic Manager', self)
        manageTopicsButton.triggered.connect(self.manage_topics)
        setMenu.addAction(companyButton)
        setMenu.addAction(manageTopicsButton)

        # Account:
        accMenu = mainMenu.addMenu('Account')  # Add account menu
        passButton = QAction('Change Password', self)
        passButton.triggered.connect(self.change_password)
        accMenu.addAction(passButton)

        # Help:
        helpMenu = mainMenu.addMenu('Help')  # Add help menu
        guideButton = QAction('User Guide', self)
        guideButton.triggered.connect(self.user_guide)
        helpMenu.addAction(guideButton)
        aboutButton = QAction('About', self)
        aboutButton.triggered.connect(self.about)
        helpMenu.addAction(aboutButton)

    def manage_topics(self):
        # Show tab manager popup if not already being shown
        if self.TopicManagerPopUp.isHidden():
            self.TopicManagerPopUp.show()

    @staticmethod
    def check_connection():
        # Check connection to Twitter
        from scraper import Scraper

        # If connection not created, show error pop up
        if not Scraper.connection_created:
            connectionPopUp = QMessageBox()
            connectionPopUp.setStandardButtons(QMessageBox.Ok)
            connectionPopUp.setIcon(QMessageBox.Warning)
            connectionPopUp.setWindowTitle("Twitter connection error")
            connectionPopUp.setText("Twitter data not available at this time. Check your internet "
                                    "connection and try again later.")
            connectionPopUp.exec_()

    def change_company(self):
        # Show company manager popup if not already being shown
        if self.CompanyManagerPopUp.isHidden():
            self.CompanyManagerPopUp.show()

    @staticmethod
    def user_guide():
        # Create the user guide window
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        # Add the text to the window
        msg.setText("Guide to using this software")
        msg.setInformativeText("The company dashboard is automatically provided upon logging in.\n"
                               "New topic tabs can be added by using the Topic Manager in the settings menu.\nThis is "
                               "done by typing the name of the topic and submitting.\nTopics can be "
                               "removed using the button on the Topic Manager."
                               "\n\n\n"
                               "Other things to note when using this software:"
                               "\n\n"
                               "1. You can add as many topics as you can fit tabs on the window."
                               "\n\n"
                               "2. Each tab you add is automatically updated and shown when logging in in future."
                               "\n\n"
                               "3. WARNING: Requesting analysis of too many topics will lead to slowing of the "
                               "application."
                               "\n\n"
                               "4. You can change the time scale on the graphs shown using the button in the top "
                               "right of the tab. "
                               "\n\n"
                               "5. Everything else is done for you!")

        # Give the text a font
        font = QFont()
        font.setBold(True)
        msg.setFont(font)

        # Set window title
        msg.setWindowTitle("User guide")

        # Allow the window to run independently from the main window
        _ = msg.exec_()

    @staticmethod
    def about():
        # Create the about window
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        # Add the text to the window
        msg.setText("Twitter Sentiment Analysis")
        msg.setText("This is a tool demonstrating the ability of sentiment analysis to provide insights into the" 
                    " opinions of Twitter users on a range of topics."
                    "\n\n"
                    "Written in Python using a Bayesian Classifier model."
                    "\n\n"
                    "Created by Lewis Clifton (2020/2021)")

        # Give the text a font
        font = QFont()
        font.setBold(True)
        msg.setFont(font)

        # Set window title
        msg.setWindowTitle("About")

        # Allow the window to run independently from the main window
        _ = msg.exec_()

    def sign_out(self):
        # Close the main window
        self.close()

        # Wait for 0.25 seconds before showing the login window
        time.sleep(0.25)

        # Deleted any entered text on the login and signup windows
        self.parent.login.username.setText("")
        self.parent.login.password.setText("")
        self.parent.signup.username.setText("")
        self.parent.signup.password.setText("")
        self.parent.signup.company.setText("")
        self.parent.show_login()
        self.parent.widget.show()

        # Reset the current user of the system
        self.parent.user = None

    def save(self):
        # Get the current date
        date = datetime.now().strftime("%d-%m-%Y")

        # Create a directory to store the screenshot if not already created
        if not os.path.exists(f"SavedData/{date}/"):
            os.makedirs(f"SavedData/{date}")

        # Get the current screen
        screen = QtWidgets.QApplication.primaryScreen()

        # Take a screenshot of the screen
        screenshot = screen.grabWindow(self.tab_widget.dashboard.winId())

        # Get the current tab
        if self.tab_widget.tabs.currentIndex() == 0:
            tab = self.tab_widget.dashboard
        else:
            tab = self.tab_widget.tabsList[self.tab_widget.tabs.currentIndex() - 1]

        # Save the screenshot of the tab with the appropriate time scale in the photo name
        if tab.timeScale == "lastWeek":
            screenshot.save(f"SavedData/{date}/{tab.name} (Last 7 Days).jpg", "jpg")
        else:
            screenshot.save(f"SavedData/{date}/{tab.name} (Last 8 Months).jpg", "jpg")

    def change_password(self):
        # Show company manager popup if not already being shown
        if self.PasswordManagerPopUp.isHidden():
            self.PasswordManagerPopUp.show()


class CompanyPopUp(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Set title of popup
        self.setWindowTitle("Change Company")

        # Set dimensions of popup
        width = 350
        height = int(width * 1 / 2)
        self.setGeometry((self.parent.width() / 2 - width / 2), (self.parent.height() / 2 - height / 2), width,
                         height)
        self.setFixedSize(width, height)

        # Create a font for the popup
        self.labelFont = QFont()
        self.labelFont.setPointSize(12)

        # Create the layout for the popup
        self.layout = QVBoxLayout()
        fieldsLayout = QFormLayout()
        self.layout.addLayout(fieldsLayout)

        # Add the input fields
        self.password = QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.newCompany = QLineEdit()
        self.companyLabel = QLabel("Enter name of new company")
        self.companyLabel.setFont(self.labelFont)
        self.passwordLabel = QLabel("Enter your password")
        self.passwordLabel.setFont(self.labelFont)
        fieldsLayout.addRow(self.passwordLabel, self.password)
        fieldsLayout.addRow(self.companyLabel, self.newCompany)

        # Add the error message to be shown when incorrect details are added
        self.errorMsg = QLabel()
        self.errorMsg.setAlignment(Qt.AlignCenter)
        self.errorMsg.setStyleSheet('color: red')
        self.errorMsg.setFont(self.labelFont)
        self.layout.addWidget(self.errorMsg)
        self.errorMsg.hide()

        # Add the cancel and confirm buttons
        self.buttonLayout = QHBoxLayout()
        self.cancel = QPushButton("Cancel")
        self.cancel.clicked.connect(self.close)
        self.cancel.setFont(self.labelFont)
        self.buttonLayout.addWidget(self.cancel)
        self.confirm = QPushButton("Change company")
        self.confirm.clicked.connect(self.change_password)
        self.confirm.setShortcut('Return')
        self.confirm.setFont(self.labelFont)
        self.buttonLayout.addWidget(self.confirm)

        # Add the layout and all of the widgets to the window
        self.layout.addLayout(self.buttonLayout)
        self.setLayout(self.layout)

    @staticmethod
    def check_if_company_valid(company):
        # Check if the given company name is valid
        if len(company) < 2 or len(company) > 30:
            return False
        else:
            return True

    def change_password(self):
        # Get the entered company and password
        new_company = self.newCompany.text()
        password = self.password.text()

        # Check if the entered company name is valid and check if their password is valid
        company_valid = self.check_if_company_valid(new_company)
        credentials_valid = Database.authenticate(self.parent.user.username, password)

        # Check if they have entered a valid company name and the password they entered is correct
        if credentials_valid:
            if company_valid:
                Database.change_company(self.parent.user.username, new_company)
                self.errorMsg.setText("Company change has been successful")
                self.errorMsg.setStyleSheet("color:green")
                self.errorMsg.show()
            else:
                self.errorMsg.setText("Please enter a valid company name")
                self.errorMsg.setStyleSheet("color:red")
                self.errorMsg.show()
        else:
            self.errorMsg.setText("The entered password is invalid")
            self.errorMsg.setStyleSheet("color:red")
            self.errorMsg.show()


class PasswordPopUp(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Set title of popup
        self.setWindowTitle("Change Password")

        # Set dimensions of popup
        width = 350
        height = int(width * 1 / 2)
        self.setGeometry((self.parent.width() / 2 - width / 2), (self.parent.height() / 2 - height / 2), width,
                         height)
        self.setFixedSize(width, height)

        # Create the layout for the popup
        self.layout = QVBoxLayout()
        fieldsLayout = QFormLayout()
        self.layout.addLayout(fieldsLayout)

        # Create a font for the popup
        self.labelFont = QFont()
        self.labelFont.setPointSize(12)

        # Add the input fields
        self.username = QLineEdit()
        self.currentPassword = QLineEdit()
        self.currentPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.newPassword = QLineEdit()
        self.newPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPassword = QLineEdit()
        self.confirmPassword.setEchoMode(QtWidgets.QLineEdit.Password)

        currentPasswordLabel = QLabel("Current password")
        currentPasswordLabel.setFont(self.labelFont)
        newPasswordLabel = QLabel("New password")
        newPasswordLabel.setFont(self.labelFont)
        confirmPasswordLabel = QLabel("Confirm new password")
        confirmPasswordLabel.setFont(self.labelFont)

        fieldsLayout.addRow(currentPasswordLabel, self.currentPassword)
        fieldsLayout.addRow(newPasswordLabel, self.newPassword)
        fieldsLayout.addRow(confirmPasswordLabel, self.confirmPassword)

        # Add the error message to be shown when incorrect details are added
        self.errorMsg = QLabel()
        self.errorMsg.setFixedHeight(30)
        self.errorMsg.setAlignment(Qt.AlignCenter)
        self.errorMsg.setStyleSheet('color: red')
        self.errorMsg.setFont(self.labelFont)
        self.layout.addWidget(self.errorMsg)
        self.errorMsg.hide()

        # Add the cancel and confirm buttons
        self.buttonLayout = QHBoxLayout()
        self.cancel = QPushButton("Cancel")
        self.cancel.clicked.connect(self.close)
        self.cancel.setFont(self.labelFont)
        self.buttonLayout.addWidget(self.cancel)
        self.confirm = QPushButton("Change password")
        self.confirm.clicked.connect(self.change_password)
        self.confirm.setShortcut('Return')
        self.confirm.setFont(self.labelFont)
        self.buttonLayout.addWidget(self.confirm)

        # Add the layout and all of the widgets to the window
        self.layout.addLayout(self.buttonLayout)
        self.setLayout(self.layout)

    @staticmethod
    def check_if_password_valid(password):
        # Check if the password is long enough
        valid_length = True
        if len(password) < 4:
            valid_length = False

        # Check if there is at least one special character in the password
        special_chars = "!\"£$%^&*(){}[];\':@<>,./?\|"
        contains_special = False
        for char in special_chars:
            if char in password:
                contains_special = True
                break

        # Check if there is at least one uppercase character
        contains_upper = False
        for char in password:
            if char.isupper():
                contains_upper = True
                break

        # Don't add the new details if the password isn't strong enough
        if not (valid_length and contains_special and contains_upper):
            return False
        return True

    def change_password(self):
        # Get the entered passwords
        current_password = self.currentPassword.text()
        new_password = self.newPassword.text()
        new_password_confirmed = self.confirmPassword.text()

        # Check if the new password they added is strong enough
        new_password_valid = self.check_if_password_valid(new_password)

        # Check if the password they  is their actual password
        credentials_valid = Database.authenticate(self.parent.user.username, current_password)

        # Show the necessary message on the window based on the given inputs
        if new_password == new_password_confirmed:
            if credentials_valid:
                if new_password_valid:
                    # Change the password (Run if all inputs are valid)
                    Database.change_password(self.parent.user.username, new_password)
                    self.errorMsg.setText("Password changed!")
                    self.errorMsg.setStyleSheet('color: green')
                    self.errorMsg.show()
                else:
                    # Show error (Run if their new password was too weak)
                    self.errorMsg.setText("New password is not strong enough")
                    self.errorMsg.setStyleSheet('color: red')
                    self.errorMsg.show()

            else:
                # Show error (Run if the current password they entered is wrong)
                self.errorMsg.setText("The entered password is invalid")
                self.errorMsg.setStyleSheet('color: red')
                self.errorMsg.show()
        else:
            # Show error (The two new passwords don't match)
            self.errorMsg.setText("Passwords do not match")
            self.errorMsg.setStyleSheet('color: red')
            self.errorMsg.show()

        # Reset input fields
        self.currentPassword.setText("")
        self.newPassword.setText("")
        self.confirmPassword.setText("")


class TopicManagerPopUp(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Set title of popup
        self.setWindowTitle("Topic Manager")

        # Set dimensions of popup
        width = 500
        height = int(width * 9 / 16)
        self.setGeometry((self.parent.width() / 2 - width / 2), (self.parent.height() / 2 - height / 2), width, height)
        self.setFixedSize(width, height)

        # Create a font to apply to all of the text on screen
        self.labelFont = QFont()
        self.labelFont.setPointSize(13)

        # Create the layout for the popup
        self.popUpLayout = QGridLayout()
        self.setLayout(self.popUpLayout)

        # Add the layout for creating a new topic
        newTopicLayout = QVBoxLayout()
        newTopicLayout.setAlignment(Qt.AlignVCenter)

        newGroupBox = QGroupBox("New Topic")
        newGroupBox.setFont(self.labelFont)
        newGroupBox.setAlignment(Qt.AlignHCenter)

        self.hint = QLabel()
        self.hint.setText("Enter name of topic here:")
        self.hint.setStyleSheet("color:grey;")
        self.hint.setFont(self.labelFont)
        newTopicLayout.addWidget(self.hint)

        self.newTopicField = QLineEdit()
        newTopicLayout.addWidget(self.newTopicField)

        newTopicButton = QPushButton("Add new topic")
        newTopicButton.setFont(self.labelFont)
        newTopicButton.clicked.connect(self.new_topic)
        newTopicButton.setShortcut('Return')
        newTopicLayout.addWidget(newTopicButton)

        newGroupBox.setLayout(newTopicLayout)

        newScrollBox = QScrollArea()
        newScrollBox.setWidget(newGroupBox)
        newScrollBox.setWidgetResizable(True)

        self.popUpLayout.addWidget(newScrollBox, 0, 1)

        # Add the layout showing the current topics
        self.update_topics_shown()

    def remove_topic(self, button_id):
        # Iterate through the buttons
        for index, button in enumerate(self.buttonList):
            if button_id == button:
                # Remove the topic on the row the button was clicked
                if index < len(self.parent.user.topics):
                    self.parent.user.remove_topic(self.parent.user.topics[index])

        # Update the main window tabs
        self.parent.tab_widget.update_tabs()
        self.update_topics_shown()

    def new_topic(self):
        # Get the name of the new entered topic
        topicName = self.newTopicField.text()
        self.newTopicField.setText("")

        # Check if topic already exists
        if topicName.lower() not in [str(topic.name).lower() for topic in self.parent.user.topics] and topicName != "":
            # Create the new topic
            self.parent.user.new_topic(topicName.lower())

            # Update the main window tabs
            self.parent.tab_widget.update_tabs()
        self.update_topics_shown()

    def update_topics_shown(self):
        # Get the current user topics
        topics = self.parent.user.topics

        topicFormLayout = QFormLayout()
        self.buttonList = []

        # Add each of the topics with a remove button next to them
        for index, topic in enumerate(topics):
            removeTopicButton = QPushButton("Remove")
            removeTopicButton.setFont(self.labelFont)
            removeTopicButton.clicked.connect(lambda: self.remove_topic(self.sender()))
            self.buttonList.append(removeTopicButton)
            topicFormLayout.insertRow(index, QLabel(f"{topic.name}"), removeTopicButton)

        # Add the box showing the topics
        self.removalGroupBox = QGroupBox("Existing Topics")
        self.removalGroupBox.setFont(self.labelFont)
        self.removalGroupBox.setAlignment(Qt.AlignHCenter)

        self.removalScroll = QScrollArea()
        self.removalScroll.setWidgetResizable(True)

        # Add the layout for viewing and removing existing topics
        self.removalGroupBox.setLayout(topicFormLayout)

        # Add the scroll box to the window
        self.removalScroll.setWidget(self.removalGroupBox)

        # Add to the window
        self.popUpLayout.addWidget(self.removalScroll, 0, 0)


class TabHandler(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.parent = parent

        # Create a layout to put all of the tabs on
        self.tabLayout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)

        # Add the dashboard
        self.dashboard = Dashboard(self.parent.user.company)
        self.tabs.addTab(self.dashboard, "Dashboard")

        # Create tabs based on the user's current topics
        self.tabsList = []
        for topic in self.parent.user.topics:
            self.add_new_tab(topic)

        # Add all of the tabs to the tab layout
        self.tabLayout.addWidget(self.tabs)

        # Place the tab layout on the window
        self.setLayout(self.tabLayout)

    def add_new_tab(self, topic):  # Add a tab
        # Create the new tab
        newTab = TopicTab(topic)
        self.tabs.addTab(newTab, str(topic.name).title())
        self.tabsList.append(newTab)

    def remove_tab(self, tab):  # Add a tab
        # Remove the tab
        self.tabs.removeTab(self.tabsList.index(tab) + 1)
        self.tabsList.remove(tab)

    def update_tabs(self):

        # Adding tabs
        for topic in self.parent.user.topics:
            if topic.name.lower() not in [tab.name.lower() for tab in self.tabsList]:
                self.add_new_tab(topic)

        # Deleting tabs
        for tab in self.tabsList:
            if tab.name.lower() not in [topic.name.lower() for topic in self.parent.user.topics]:
                self.remove_tab(tab)


class Tab(QWidget):
    def __init__(self, topic):
        super(Tab, self).__init__()

        # Get all of the details of the topic to be shown
        self.name = topic.name

        # Establish the time scale of the graphs being shown (last 7 days or last 8 months)
        self.timeScale = "lastWeek"

        # Data from the analyses that took place upon logging in
        self.tweets = topic.tweets
        self.likes = topic.likes
        self.authors = topic.authors
        self.predictions = topic.predictions
        self.sentiments = topic.sentiments

        # Get the topic data from last 7 days/last 8 months
        self.historicalAverageSentiment = topic.historicalAverageSentiment
        self.monthsTweets = topic.monthsTweets[::-1]
        self.monthsAverageSentiments = topic.monthsAverageSentiments[::-1]
        self.monthsAveragePosNegTweets = topic.monthsAveragePosNegTweets[::-1]
        self.lastWeeksTweets = topic.lastWeeksTweets[::-1]
        self.lastWeeksAverageSentiments = topic.lastWeeksAverageSentiments[::-1]
        self.lastWeeksAveragePosNegTweets = topic.lastWeeksAveragePosNegTweets[::-1]

        # Initialise the UI components of the tab
        self.initUI()

    def initUI(self):

        self.windowLayout = QVBoxLayout()

        # Add all the widgets for the top layout
        self.topLayout = QHBoxLayout()

        labelFont = QFont()
        labelFont.setPointSize(12)

        nameLabel = QLabel(f"Showing Twitter data on: {str(self.name)}")
        nameLabel.setFont(labelFont)
        self.topLayout.addWidget(nameLabel)

        averageLabel = QLabel(f"Historical Average Sentiment: {str(self.historicalAverageSentiment)}")
        averageLabel.setFont(labelFont)
        self.topLayout.addWidget(averageLabel)

        if len(self.tweets) != 0:
            tweetsLabel = QLabel(f"No. recent tweets: {str(len(self.tweets))}")
            tweetsLabel.setFont(labelFont)
            self.topLayout.addWidget(tweetsLabel)

            authorsLabel = QLabel(f"No. unique tweet authors: {str(len(set(self.authors)))}")
            authorsLabel.setFont(labelFont)
            self.topLayout.addWidget(authorsLabel)

        self.scaleButton = QPushButton("Show Last 8 Months")
        self.scaleButton.setFixedWidth(150)
        self.scaleButton.clicked.connect(self.change_time_scale)
        self.scaleButton.setFont(labelFont)
        self.topLayout.addWidget(self.scaleButton)
        self.windowLayout.addLayout(self.topLayout)

        # Create the bottom layout
        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setAlignment(Qt.AlignLeft)

        # Add the charts/graphs to the tab
        self.graphLayout = QGridLayout()

        # # Add the graphs showing data from the last 8 months
        self.timeSeriesLayout = QGridLayout()
        self.plot_tweets_over_time()
        self.plot_pos_neg_over_time()
        self.plot_sent_over_time()
        self.graphLayout.addLayout(self.timeSeriesLayout, 0, 0)

        self.currentDataLayout = QGridLayout()
        # # Add the data from the most recent analysis
        if len(self.predictions) != 0:
            # Add the tweet scroll box showing recent tweets
            self.add_scroll_box()

            # Add word cloud and pie chart
            self.currentDataLayout.setAlignment(Qt.AlignLeft)
            self.plot_pos_vs_neg()
            self.plot_word_cloud()
        self.graphLayout.addLayout(self.currentDataLayout, 1, 0)

        # Combine layouts
        self.bottomLayout.addLayout(self.graphLayout)
        self.windowLayout.addLayout(self.bottomLayout)

        # Add the layouts to the window
        self.setLayout(self.windowLayout)

    def change_time_scale(self):
        # Change the time scale of the graphs being shown
        if self.timeScale == "year":
            self.timeScale = "lastWeek"
            self.scaleButton.setText("Show Last 8 Months")
        else:
            self.timeScale = "year"
            self.scaleButton.setText("Show Last 7 Days")

        # Plot the updated graphs
        self.plot_tweets_over_time()
        self.plot_pos_neg_over_time()
        self.plot_sent_over_time()

    def add_scroll_box(self):

        # Create a scroll box containing tweets about the topic/company
        formLayout = QFormLayout()
        groupBox = QGroupBox("Tweets")
        groupBox.setMaximumWidth(550)

        # Order the tweets according to how many likes they have
        zippedTweets = zip(self.tweets, self.likes, self.authors)
        zippedTweetsList = list(zippedTweets)
        sortedTweets = sorted(zippedTweetsList, key=lambda x: x[1], reverse=True)

        # Add the ordered tweets to the layout
        for i in range(len(sortedTweets)):
            # Add the tweets with their authors and likes with font size 10
            labelFont = QFont()
            labelFont.setPointSize(10)
            tweetAuthor = QLabel(f"@{sortedTweets[i][2]} ({sortedTweets[i][1]} likes):")
            tweetAuthor.setFont(labelFont)
            tweetText = QLabel(sortedTweets[i][0], wordWrap=True, alignment=Qt.AlignLeft | Qt.AlignTop)
            tweetText.setFont(labelFont)
            formLayout.addRow(tweetAuthor, tweetText)
        groupBox.setLayout(formLayout)

        # Create a scroll box to put the tweets in
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumWidth(550)
        scroll.setWidget(groupBox)

        # Add this scroll box to the window
        self.bottomLayout.addWidget(scroll)

    def plot_pos_neg_over_time(self):

        # Create bars to go on the bar chart
        posBar = QBarSet("Positive")
        posBar.setColor(Qt.green)
        posBar.setPen(QPen(Qt.black, 2))
        negBar = QBarSet("Negative")
        negBar.setColor(Qt.red)
        negBar.setPen(QPen(Qt.black, 2))

        # Add the data
        if self.timeScale == "year":
            for month in self.monthsAveragePosNegTweets:
                posBar << month[0]
                negBar << month[1]
            xLabels = [(datetime.now() - timedelta(days=30 * i)).strftime("%m/%y") for i in range(8)][::-1]
            timeScale = "Month"
        else:
            for day in self.lastWeeksAveragePosNegTweets:
                posBar << day[0]
                negBar << day[1]
            xLabels = [(datetime.now() - timedelta(days=i)).strftime("%d/%m") for i in range(0, 7)][::-1]
            timeScale = "Day"

        # Add the data
        series = QBarSeries()
        series.append(posBar)
        series.append(negBar)

        # Create the bar chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Positive vs Negative Tweets")
        chartFont = QFont()
        chartFont.setPointSize(10)
        chart.setFont(chartFont)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartThemeLight)

        # Add the y-axis
        axisY = QValueAxis()
        axisY.setLabelFormat("%i")
        axisY.setTitleText("No. Tweets")
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        chart.axisY(series).setRange(0, (
                int(math.ceil(max([max(item) for item in self.monthsAveragePosNegTweets]) / 100)) * 100))

        # Add the x-axis
        axisX = QBarCategoryAxis()
        axisX.append(xLabels)
        axisX.setTitleText(timeScale)
        chart.setAxisX(axisX, series)

        # Show the legend
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        # Add the chart to the window
        chartView = QChartView(chart)
        chartView.setMinimumSize(100, 100)
        self.timeSeriesLayout.addWidget(chartView, 0, 0)

    def plot_pos_vs_neg(self):

        # Add a pie chart comparing positive and negative tweets from the most recent analysis
        series = QPieSeries()

        # Get the data to put on the pie chart
        pos_percent = neg_percent = 0
        if len(self.tweets) != 0:
            pos_percent = round(self.sentiments.count("Positive") / len(self.sentiments), 2) * 100
            neg_percent = 100 - pos_percent
        series.append("Positive", pos_percent)
        series.append("Negative", neg_percent)

        # Add the positive pie slice
        slice = QPieSlice()
        slice = series.slices()[0]
        slice.setPen(QPen(Qt.black, 2))
        slice.setBrush(Qt.green)

        # Add the negative pie slice
        slice = QPieSlice()
        slice = series.slices()[1]
        slice.setPen(QPen(Qt.black, 2))
        slice.setBrush(Qt.red)

        # Create the pie chart
        chart = QChart()
        chart.legend()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chartFont = QFont()
        chartFont.setPointSize(10)
        chart.setFont(chartFont)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Positive vs Negative Tweets")

        # Add the legend to the pie chart
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        # Add the chart to the window
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        chartView.setMinimumSize(100, 100)
        chartView.setMaximumWidth(500)
        self.currentDataLayout.addWidget(chartView, 1, 0)

    def plot_tweets_over_time(self):

        # Create a line graph showing the average number of tweets per month
        series = QLineSeries()

        # Create the data to go on the graph
        if self.timeScale == "year":
            data = [QPoint(month, noTweets) for month, noTweets in enumerate(self.monthsTweets)]
            xLabels = [(datetime.now() - timedelta(days=30 * i)).strftime("%m/%y") for i in range(8)][::-1]
            timeScale = "Month"
        else:
            data = [QPoint(day, noTweets) for day, noTweets in enumerate(self.lastWeeksTweets)]
            xLabels = [(datetime.now() - timedelta(days=i)).strftime("%d/%m") for i in range(0, 7)][::-1]
            timeScale = "Day"
        series.append(data)

        # Create the graph
        chart = QChart()
        chart.addSeries(series)
        chartFont = QFont()
        chartFont.setPointSize(10)
        chart.setFont(chartFont)
        chart.setTitle(f'Number of people tweeting about {self.name}')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # Add the x-axis
        axisX = QBarCategoryAxis()
        axisX.append(xLabels)
        axisX.setTitleText(timeScale)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        # Add the y-axis
        axisY = QValueAxis()
        axisY.setLabelFormat("%i")
        axisY.setTitleText("No. Tweets")
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        chart.axisY(series).setRange(0, (int(math.ceil(max(self.monthsTweets) / 100)) * 100))

        # Hide the legend
        chart.legend().hide()

        # Add the chart to the window
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        chartView.setMinimumSize(100, 100)
        self.timeSeriesLayout.addWidget(chartView, 0, 2)

    def plot_sent_over_time(self):

        # Create a line graph showing the average number of tweets per month
        series = QLineSeries()

        # Create the data
        if self.timeScale == "year":
            data = [QPoint(month, int(sentiment * 100)) for month, sentiment in enumerate(self.monthsAverageSentiments)]
            timeScale = "Month"
            xLabels = [(datetime.now() - timedelta(days=30 * i)).strftime("%m/%y") for i in range(8)][::-1]
        else:
            data = [QPoint(day, int(sentiment * 100)) for day, sentiment in enumerate(self.lastWeeksAverageSentiments)]
            timeScale = "Day"
            xLabels = [(datetime.now() - timedelta(days=i)).strftime("%d/%m") for i in range(0, 7)][::-1]
        series.append(data)

        # Create the graph
        chart = QChart()
        chart.addSeries(series)
        chartFont = QFont()
        chartFont.setPointSize(10)
        chart.setFont(chartFont)
        chart.setTitle(f'Average sentiment of tweets over time')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # Add the x-axis
        axisX = QBarCategoryAxis()
        axisX.append(xLabels)
        axisX.setTitleText(timeScale)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        # Add the quantitative y-axis
        axisY = QValueAxis()
        axisY.setLabelFormat("%i")
        axisY.setTickCount(3)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        chart.axisY(series).setRange(0, (int(math.ceil(max(self.monthsAverageSentiments) / 100)) * 100))
        axisY.hide()

        # Replace the y-axis with qualitative labels
        yLabels = ["Negative", "Neutral", "Positive"]
        axisY = QBarCategoryAxis()
        axisY.append(yLabels)
        axisY.setTitleText("Sentiment")
        chart.addAxis(axisY, Qt.AlignLeft)
        axisY.show()

        # Hide the legend
        chart.legend().hide()

        # Add the graph to the window
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        chartView.setMinimumSize(100, 100)
        self.timeSeriesLayout.addWidget(chartView, 0, 1)

    def plot_word_cloud(self):
        # Get the tweets ready for the word cloud
        tweets = [
            " ".join([word.strip() for word in tweet.split() if len(word) > 2 and "https" not in word and word != "RT"])
            for tweet in self.tweets]

        tweets = " ".join(tweets)
        # Create the canvas to put the wordcloud
        self.canvas = FigureCanvas(Figure(figsize=(5, 3), frameon=False))
        self.axes = self.canvas.figure.add_subplot(frameon=False, xticks=[], yticks=[])

        # Create the wordcloud and add it to the canvas
        wordcloud = WordCloud(random_state=21, max_font_size=50, max_words=40, collocations=False,
                              prefer_horizontal=1, colormap="Blues", background_color="white").generate(tweets)
        self.axes.imshow(wordcloud)

        # Add the wordcloud to the tab
        self.currentDataLayout.addWidget(self.canvas, 1, 1)


class Dashboard(Tab):
    def __init__(self, company):
        super().__init__(company)


class TopicTab(Tab):
    def __init__(self, topic):
        super().__init__(topic)


class Login(QDialog):  # Inherits QDialog so the window can be put on the stack widget
    def __init__(self, parent):  # The parent parameter is the stack widget
        super(Login, self).__init__()
        self.parent = parent  # Gives the login instance access to change the stack widget

    def initUI(self):  # Initialise the UI

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
        loginButton.setShortcut('Return')
        loginButton.clicked.connect(self.login)

        signupButton = QPushButton("Sign Up")
        signupButton.setFixedWidth(100)
        signupButton.clicked.connect(self.signUp)

        buttonLayout.addWidget(loginButton)
        buttonLayout.addSpacing(50)
        buttonLayout.addWidget(signupButton)

        # Add a checkboc
        # self.signedInCB = QCheckBox('Keep me signed in', self)

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
        signupButton.setShortcut('Return')
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

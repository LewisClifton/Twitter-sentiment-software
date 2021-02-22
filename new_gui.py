from matplotlib.backends.backend_template import FigureCanvas

from database import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPalette, QColor, QKeySequence, QLinearGradient, QGradient, QBrush
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, \
    QMainWindow, QAction, QWidget, QTabWidget, QLabel, QGroupBox, QScrollArea, QGridLayout, QMessageBox, QInputDialog, \
    QShortcut
from PyQt5 import Qt
from PyQt5.QtCore import Qt, QPoint
import time
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice, QPercentBarSeries, QBarCategoryAxis, QBarSet, \
    QLineSeries, QCategoryAxis, QValueAxis, QDateTimeAxis, QBarSeries
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt


from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import numpy as np
import math

def get_screen_size():
    sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
    return sizeObject.width(), sizeObject.height()


class MainWindow(QMainWindow):
    def __init__(self, parent, user):
        super(MainWindow, self).__init__()
        self.parent = parent

        self.user = user

    def initUI(self):  # Initialise the UI
        self.setWindowTitle('Sentiment Analysis')

        # Establish geometry
        width = 1500
        height = int(width * 2 / 3)

        # Centre the window
        self.setGeometry(get_screen_size()[0] / 2 - width / 2, get_screen_size()[1] / 2 - height / 2, 0, 0)

        # Set fixed dimensions for the window so the user can't accidentally change the window size
        # self.setFixedSize(width, height)

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
        saveButton.triggered.connect(self.save)
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
        # prefMenu.addAction(colButton)

        # Settings:
        setMenu = mainMenu.addMenu('Settings')  # Add settings menu
        companyButton = QAction('Company', self)
        removeTopicsButton = QAction('Remove Topic', self)
        removeTopicsButton.triggered.connect(self.remove_topic)
        setMenu.addAction(companyButton)
        setMenu.addAction(removeTopicsButton)

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
        # Create a popup where the user can enter the name of their new company
        enteredCompany, textEntered = QInputDialog.getText(self, 'Change company', 'Enter company name:')

        # Run if the user enters a new company
        if textEntered:

            self.user.change_company(enteredCompany)
            self.sign_out()

    def new(self):
        # Create a popup where the user can enter the name of a new topic they want to analyse
        topicName, text_entered = QInputDialog.getText(self, 'New topic', 'Enter topic name:')

        # Run if the user enters a topic
        if text_entered:
            # Only add the topic if it doesn't already exist in the user's topic list
            if topicName.lower() not in [str(topic.name).lower() for topic in self.parent.user.topics]:
                self.parent.user.new_topic(topicName.lower())
                self.tab_widget.update_tabs()

    def remove_topic(self):
        # Create a popup where the user can enter the name of the topic they no longer need
        enteredTopicName, textEntered = QInputDialog.getText(self, 'Remove topic', 'Enter topic name:')

        # Run if the user enters a topic
        if textEntered:

            # Remove this topic tab
            for userTopic in self.user.topics:
                if enteredTopicName.lower() == userTopic.name:
                    self.user.remove_topic(userTopic)

            # Update the tabs being shown on screen
            self.tab_widget.update_tabs()

    def user_guide(self):
        pass

    def about(self):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Twitter Sentiment Analysis")
        msg.setInformativeText("Created by Lewis Clifton")
        msg.setWindowTitle("About")

        _ = msg.exec_()

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

    def save(self):
        screen = QtWidgets.QApplication.primaryScreen()
        for tab in self.tab_widget.tabsList:
            rect = tab.geometry()
            x = rect.x()
            y = rect.y()
            w = rect.width()
            h = rect.height()
            screenshot = screen.grabWindow(tab.winId(), x, y, w, h) 
            screenshot.save('shot.jpg', 'jpg')


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
        self.tabs.removeTab(self.tabsList.index(tab)+1)
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

        self.timeScale = "week"

        self.tweets = topic.tweets
        self.likes = topic.likes
        self.authors = topic.authors

        self.predictions = topic.predictions
        self.sentiments = topic.sentiments

        self.historicalAverageSentiment = topic.historicalAverageSentiment
        self.monthsTweets = topic.monthsTweets[::-1]
        self.monthsAverageSentiments = topic.monthsAverageSentiments[::-1]
        self.monthsAveragePosNegTweets = topic.monthsAveragePosNegTweets[::-1]
        self.lastWeeksTweets = topic.lastWeeksTweets[::-1]
        self.lastWeeksAverageSentiments = topic.lastWeeksAverageSentiments[::-1]
        self.lastWeeksAveragePosNegTweets = topic.lastWeeksAveragePosNegTweets[::-1]


        self.initUI()


    def initUI(self):
        self.windowLayout = QVBoxLayout()

        # Add the top layout
        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(QLabel(str(self.name)))
        self.topLayout.addWidget(QLabel(f"Historical Average Sentiment: {str(self.historicalAverageSentiment)}"))
        self.topLayout.addWidget(QLabel(f"Current number of tweets: {str(len(self.tweets))}"))
        self.topLayout.addWidget(QLabel(f"Number of unique tweet authors: {str(len(set(self.authors)))}"))
        self.scaleButton = QPushButton("Show Last 8 Months")
        self.scaleButton.setFixedWidth(150)
        self.scaleButton.clicked.connect(self.change_time_scale)
        self.topLayout.addWidget(self.scaleButton)
        self.windowLayout.addLayout(self.topLayout)

        # Create the bottom layout
        self.bottomLayout = QHBoxLayout()

        # Add the scroll box
        self.add_scroll_box()

        # Add the necessary graphs
        self.graphLayout = QGridLayout()
        self.plot_pos_vs_neg()
        self.plot_tweets_over_time()
        self.plot_pos_neg_over_time()
        self.plot_sent_over_time()
        self.bottomLayout.addLayout(self.graphLayout)

        self.windowLayout.addLayout(self.bottomLayout)

        # Add the layouts to the window
        self.setLayout(self.windowLayout)

    def change_time_scale(self):
        if self.timeScale == "year":
            self.timeScale = "lastWeek"
            self.scaleButton.setText("Show Last 8 Months")
        else:
            self.timeScale = "year"
            self.scaleButton.setText("Show Last 7 Days")

        self.plot_pos_vs_neg()
        self.plot_tweets_over_time()
        self.plot_pos_neg_over_time()
        self.plot_sent_over_time()

    def add_scroll_box(self):
        # Create a scroll box containing tweets about the topic/company
        formLayout = QFormLayout()
        groupBox = QGroupBox("Tweets")

        # Add the tweets to the scroll box in order of how many likes they have
        zippedTweets = zip(self.tweets, self.likes, self.authors)
        zippedTweetsList = list(zippedTweets)
        sortedTweets = sorted(zippedTweetsList, key=lambda x: x[1], reverse=True)

        if len(sortedTweets) != 0:
            for i in range(len(sortedTweets)):
                formLayout.addRow(QLabel(f"@{sortedTweets[i][2]} ({sortedTweets[i][1]} likes):"),
                                  QLabel(sortedTweets[i][0]))
            groupBox.setLayout(formLayout)
        else:
            vbox = QHBoxLayout()
            vbox.addWidget(QLabel("Tweets not availble. Please try again later"))
            vbox.setAlignment(Qt.AlignCenter)
            groupBox.setLayout(vbox)

        # Add the scroll box to the window
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
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
            xLabels = [(datetime.now() - timedelta(days=30*i)).strftime("%m/%y") for i in range(0, 8)][::-1]
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
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartThemeLight)

        # Add the y-axis
        axisY = QValueAxis()
        axisY.setLabelFormat("%i")
        axisY.setTitleText("No. Tweets")
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        chart.axisY(series).setRange(0, (int(math.ceil(max([max(item)for item in self.monthsAveragePosNegTweets]) / 100)) * 100))

        # Add the x-axis
        axisX = QBarCategoryAxis()
        axisX.append(xLabels)
        axisX.setTitleText(timeScale)
        chart.setAxisX(axisX, series)

        # Show the legend
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        # Add the chart to the window
        chartview = QChartView(chart)
        self.graphLayout.addWidget(chartview, 0, 0)

    def plot_pos_vs_neg(self):

        # Add a pie chart comparing positive and negative tweets
        series = QPieSeries()

        # Get the data to put on the pie chart
        pos_percent = neg_percent = 0
        if len(self.tweets) != 0:
            pos_percent = round(self.sentiments.count("Positive")/len(self.sentiments),2)*100
            neg_percent = 100-pos_percent
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
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Positive vs Negative Tweets")

        # Add the legend to the pie chart
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        # Add the chart to the window
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        self.graphLayout.addWidget(chartView,0,1)


    def plot_tweets_over_time(self):

        # Create a line graph showing the average number of tweets per month
        series = QLineSeries()

        # Create the data to go on the graph
        if self.timeScale == "year":
            data = [QPoint(month, noTweets) for month, noTweets in enumerate(self.monthsTweets)]
            xLabels = [(datetime.now() - timedelta(days=30*i)).strftime("%m/%y") for i in range(0, 8)][::-1]
            timeScale = "Month"
        else:
            data = [QPoint(day, noTweets) for day, noTweets in enumerate(self.lastWeeksTweets)]
            xLabels = [(datetime.now() - timedelta(days=i)).strftime("%d/%m") for i in range(0, 7)][::-1]
            timeScale = "Day"
        series.append(data)

        # Create the graph
        chart = QChart()
        chart.addSeries(series)
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
        self.graphLayout.addWidget(chartView, 1, 0)

    def plot_sent_over_time(self):

        # Create a line graph showing the average number of tweets per month
        series = QLineSeries()

        # Create the data
        if self.timeScale == "year":
            data = [QPoint(month, int(sentiment*100)) for month, sentiment in enumerate(self.monthsAverageSentiments)]
            timeScale = "Month"
            xLabels = [(datetime.now() - timedelta(days=30*i)).strftime("%m/%y") for i in range(0, 8)][::-1]
        else:
            data = [QPoint(day, int(sentiment*100)) for day, sentiment in enumerate(self.lastWeeksAverageSentiments)]
            timeScale = "Day"
            xLabels = [(datetime.now() - timedelta(days=i)).strftime("%d/%m") for i in range(0, 7)][::-1]
        series.append(data)

        # Create the graph
        chart = QChart()
        chart.addSeries(series)
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
        self.graphLayout.addWidget(chartView, 1, 1)




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

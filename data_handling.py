from scraper import Scraper
from database import *
from model import Model


class TopicHandler:
    def __init__(self, id, name):
        # Topic info attributes
        self.id = id
        self.name = name

        # Topic tweets attributes
        self.tweets = []
        self.likes = []
        self.authors = []

        # Data from current analysis
        self.predictions = []
        self.sentiments = []
        self.posTweets = 0
        self.negTweets = 0
        self.currentSentiment = 0.5

        # Log data
        self.historicalAverageSentiment = 0.5
        self.monthsTweets = [0 for i in range(8)]
        self.monthsAverageSentiments = [0.5 for i in range(8)]
        self.monthsAveragePosNegTweets = [0 for i in range(8)]
        self.lastWeeksTweets = [0 for i in range(7)]
        self.lastWeeksAverageSentiments = [0.5 for i in range(7)]
        self.lastWeeksAveragePosNegTweets = [0 for i in range(7)]

    def perform_analysis(self):
        # Get the tweets and perform analysis on these tweets
        self.get_tweets()
        self.get_predictions()

    def get_tweets(self):
        # Get the tweets, tweet authors and likes of the tweets
        self.tweets = Scraper.get_tweets(self.name)

        self.tweets = [tweet for tweet in self.tweets]

        self.authors = [tweet[0] for tweet in self.tweets]

        self.likes = [tweet[2] for tweet in self.tweets]

        self.tweets = list(set([tweet[1] for tweet in self.tweets]))

    def get_predictions(self):
        # Get predictions
        self.predictions, self.sentiments = Model.make_tweet_predictions(self.tweets)
        # Current average sentiment of the most recent analysis
        if len(self.predictions) != 0:
            self.currentSentiment = round(sum(self.predictions) / len(self.predictions), 2)

        # Get the number of positive and negative tweets
        self.posTweets = self.sentiments.count("Positive")
        self.negTweets = self.sentiments.count("Negative")

    def make_log(self):
        # Make a log in the database of current analysis data
        Database.make_log(self)

    def get_last_8_months(self, logs):
        # Get today's date
        date = datetime.now().strftime("%d/%m/%y").split("/")

        # Iterate through the last 8 months
        for i in range(8):
            # Get the current month
            month = (datetime.now() - timedelta(days=30 * i)).strftime("%m/%Y")

            # Calculate the average sentiment this month
            sentiments_that_month = [log[0] for log in logs if datetime.strptime(log[1], "%d/%m/%Y").strftime("%m/%Y")
                                     == month]
            if len(sentiments_that_month) != 0:
                month_average_sentiment = round(sum(sentiments_that_month) / len(sentiments_that_month), 2)
                self.monthsAverageSentiments[i] = month_average_sentiment
            else:
                self.monthsAverageSentiments[i] = 0.5

            # Calculate the average number of positive and negative tweets this month
            pos_this_month = [log[2] for log in logs if datetime.strptime(log[1], "%d/%m/%Y").strftime("%m/%Y")
                              == month]
            neg_this_month = [log[3] for log in logs if datetime.strptime(log[1], "%d/%m/%Y").strftime("%m/%Y")
                              == month]
            average_pos_this_month = average_neg_this_month = 0
            if len(pos_this_month) != 0:
                average_pos_this_month = round(sum(pos_this_month) / len(pos_this_month))
            if len(neg_this_month) != 0:
                average_neg_this_month = round(sum(neg_this_month) / len(neg_this_month))
            self.monthsAveragePosNegTweets[i] = [average_pos_this_month, average_neg_this_month]

        # Get number of tweets in each month
        self.monthsTweets = [sum(month) for month in self.monthsAveragePosNegTweets]

        # Calculate the all-time average sentiment
        if len(logs) != 0:
            self.historicalAverageSentiment = round(
                sum(self.monthsAverageSentiments) / len(self.monthsAverageSentiments),
                2)

    def get_last_week_data(self, logs):
        # Get stats from the last 7 days
        last_week_dates = [(datetime.now() - timedelta(days=i)).strftime("%d/%m/%Y") for i in range(7)]

        # Iterate through each day in the last week
        for i in range(7):
            # Get the current day
            day = last_week_dates[i]

            # Calculate the average sentiment this day
            days_sentiments = [log[0] for log in logs if log[1] == day]
            if len(days_sentiments) != 0:
                days_average_sentiment = round(sum(days_sentiments) / len(days_sentiments), 2)
                self.lastWeeksAverageSentiments[i] = days_average_sentiment
            else:
                self.lastWeeksAverageSentiments[i] = 0.5

            # Calculate the average number of positive and negative tweets on this day
            pos_tweets_this_day = [log[2] for log in logs if log[1] == day]
            neg_tweets_this_day = [log[3] for log in logs if log[1] == day]
            average_pos_this_day = average_neg_this_day = 0
            if len(pos_tweets_this_day) != 0:
                average_pos_this_day = round(sum(pos_tweets_this_day) / len(pos_tweets_this_day))
            if len(neg_tweets_this_day) != 0:
                average_neg_this_day = round(sum(neg_tweets_this_day) / len(neg_tweets_this_day))
            self.lastWeeksAveragePosNegTweets[i] = [average_pos_this_day, average_neg_this_day]

        # Get the total number of tweets in the last 7 days
        self.lastWeeksTweets = [sum(day) for day in self.lastWeeksAveragePosNegTweets]

    def get_logs(self):
        # Use the database to get the logs on this topic/company
        logs = Database.get_logs(self)

        # Retrieve from these logs the records from the last 8 months
        self.get_last_8_months(logs)

        # Retrieve from these logs the records from the last 7 days
        self.get_last_week_data(logs)


class Company(TopicHandler):  # Inherit TopicHandler class
    def __init__(self, companyID, companyName):
        # Declare that this object is specfically a company
        self.type = "company"

        # Run parent constructor
        super(Company, self).__init__(companyID, companyName)

        # Perform initial analysis
        self.perform_analysis()

        # Make a log of this data
        self.make_log()

        # Retrieve existing logs
        self.get_logs()


class Topic(TopicHandler):  # Inherit TopicHandler class
    def __init__(self, topicID, topic):
        # Declare that this object is specfically a company
        self.type = "topic"

        # Run parent constructor
        super(Topic, self).__init__(topicID, topic)

        # Perform initial analysis
        self.perform_analysis()

        # Make a log of this data
        self.make_log()

        # Retrieve existing logs
        self.get_logs()


class User:
    def __init__(self, username):
        # Establish attributes
        self.username = username
        self.id = None
        self.company = None
        self.topics = None

        self.get_info()

    def get_info(self):
        # Get the user's information including their topics and what company they belong to.
        self.id, company, companyID = Database.get_user_info(self.username)

        # Create the user's list of topics
        self.topics = [Topic(topic[0], topic[1]) for topic in Database.get_user_topics(self.id)]

        # Create a Company instance
        self.company = Company(companyID, company)

    def new_topic(self, topicName):
        # Add the new topic to the database
        topicID = Database.new_topic(self.id, topicName)

        # Create a new Topic instance
        topic = Topic(topicID, topicName)

        # Add this topic to the user's topic list
        self.topics.append(topic)

    def remove_topic(self, topic):
        # Remove the relationship between the user and the topic
        Database.remove_topic(self.id, topic.id)

        # Remove the topic from the user's list of topics
        self.topics.remove(topic)

    def change_company(self, new_company_name):
        # Change the user's associated company in the database
        Database.change_company(self.username, new_company_name)

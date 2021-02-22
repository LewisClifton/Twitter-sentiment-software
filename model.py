import pickle
# General data handling
import pandas as pd
import numpy as np

# Cleaning and preprocessing
import nltk
# nltk.download('stopwords')
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer

from sklearn.model_selection import train_test_split

# Model creation
from nltk import classify
from nltk import NaiveBayesClassifier

# Model loading
import pickle


class Model:
    # Create the tools used for cleaning
    stop_words = set(stopwords.words('english'))

    slang = {
        'u': 'you',
        'r': 'are',
        'some1': 'someone',
        'yrs': 'years',
        'hrs': 'hours',
        'mins': 'minutes',
        'secs': 'seconds',
        'pls': 'please',
        'plz': 'please',
        '2morow': 'tomorrow',
        '2day': 'today',
        '4got': 'forget',
        '4gotten': 'forget',
    }

    # Create the tools used for pre-processing
    lemmatizer = WordNetLemmatizer()

    tokenizer = TweetTokenizer(reduce_len=True)

    model = None
    model_loaded = False

    @classmethod
    def load_model(cls):
        # Load the model to be used
        model_file = open("sentiment_model.pickle", 'rb')
        cls.model = pickle.load(model_file)
        model_file.close()

        model_loaded = True

    @classmethod
    def make_tweet_predictions(cls, tweets):

        # Create a list of clean tweets
        cleaned_tweets = [cls.clean(tweet) for tweet in tweets]

        # Create a list of pre-processed tweets
        pre_processed_tweets = [cls.pre_process(tweet) for tweet in cleaned_tweets]

        # Create a list of predictions for the tweets
        predictions = [cls.make_model_prediction(tweet) for tweet in pre_processed_tweets]

        # Get the list of sentiments
        sentiments = cls.get_sentiment(predictions)

        return predictions, sentiments

    @classmethod
    def clean(cls, text):
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))

        # Remove numbers
        text = text.translate(str.maketrans('', '', '0123456789'))

        # Remove stop words
        text = [item.lower() for item in text.split() if item not in cls.stop_words]

        # Remove slang/abbreviations
        text = [cls.slang[item] if item in cls.slang.keys() else item for item in text]

        # Join the text back together
        cleaned_text = ' '.join(text)

        return text

    @classmethod
    def pre_process(cls, text):
        # Lemmatize words
        text = [cls.lemmatizer.lemmatize(item) for item in text]

        # Tokenize words
        text = cls.tokenizer.tokenize(' '.join(text))

        # Make the data into the structure readable by the model
        text = dict([item, True] for item in text)

        return text

    @classmethod
    def make_model_prediction(cls, prepared_text):
        # Use the model to make a prediction
        prediction = cls.model.classify(prepared_text)

        return prediction

    @staticmethod
    def get_sentiment(predictions):
        # Convert predictions to readable sentiments
        sentiments = ["Positive" if prediction == 1 else "Negative" for prediction in predictions]

        return sentiments


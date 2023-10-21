# Make necessary imports
import tweepy
from config import keys


class Scraper:
    # The following constants are keys which Twitter uses to authenticate my access to their Tweets
    CONSUMER_KEY = keys['CONSUMER_KEY']
    CONSUMER_SECRET = keys['CONSUMER_SECRET']
    ACCESS_TOKEN = keys['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = keys['ACCESS_TOKEN_SECRET']

    # The 4 keys are authenticated in a request to Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)  # Twitter authenticates the consumer keys
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)  # Twitter authenticates the access keys

    api = tweepy.API(auth)  # Create an API object so I can access the methods I need to view tweets


    connection_created = False # Will be used to provide necessary UI output if connection is unsuccessful

    # Check if the authorization is successfull
    try:
        connection_created = auth.get_authorization_url()
    except tweepy.TweepError:
        pass

    @classmethod
    def get_tweets(cls, topic_name, num_of_tweets=150):
        try:
            # Retrieve the tweets from the API
            scraped_tweets = tweepy.Cursor(cls.api.search, q=topic_name,
                                           lang='en', tweet_mode='extended', include_rts=False).items(num_of_tweets)

            # Storing the author, text, likes of the tweets in a list
            tweets_list = [[tweet.author.screen_name, tweet.full_text, tweet.favorite_count]for tweet in scraped_tweets]

            return tweets_list

        # Run if no tweets are available
        except BaseException as e:
            return []
import tweepy
from keys import keys


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

    # If the try block produces an error, the error statement will be output
    try:
        _ = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Failed to connect to Twitter API')

    @classmethod
    def get_tweets(cls, topic_name, num_of_tweets=150):
        try:
            # Retrieve the tweets from the API
            scraped_tweets = tweepy.Cursor(cls.api.search, q=topic_name, lang='en').items(num_of_tweets)

            # Storing the author, text, likes of the tweets in a list
            tweets_list = [[tweet.author.screen_name, tweet.text, tweet.favorite_count] for tweet in
                           scraped_tweets if not str(tweet.text).lower().startswith("rt @")]

            return tweets_list

        except BaseException as e:
            print('Failed to retrieve tweets', str(e))


# tweets = Scraper.get_tweets("Intel", 200)
#
# print(tweets)
#
# print(f"Number of tweets retrieved: {len(tweets)}")

# if ((not tweet.retweeted) and ('RT @' not in tweet.text))]
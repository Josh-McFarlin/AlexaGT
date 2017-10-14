import tweepy
import config

"""
class Tweet:
    def __init__(self):


"""

auth = tweepy.OAuthHandler(config.TW_CONSUMER_KEY, config.TW_CONSUMER_SECRET)
auth.set_access_token(config.TW_ACCESS_TOKEN_KEY, config.TW_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


def get_tweets(user_name, count):
    user = api.get_user(user_name)
    user_tweets = api.user_timeline(screen_name=user_name, count=count)
    for tweet in user_tweets:
        print(tweet.text)


get_tweets('GeorgiaTech', 3)

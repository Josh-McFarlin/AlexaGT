import tweepy
import config


auth = tweepy.OAuthHandler(config.TW_CONSUMER_KEY, config.TW_CONSUMER_SECRET)
auth.set_access_token(config.TW_ACCESS_TOKEN_KEY, config.TW_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


def get_tweets(user_name, count):
    user_tweets = api.user_timeline(screen_name=user_name, count=count)
    tweets = []
    for tweet in user_tweets:
        tweet_urls = [i['url'] for i in tweet.entities['urls']]
        txt = tweet.text
        time = tweet.created_at
        time_format = time.strftime('%B %d')
        for i in tweet_urls:
            txt = txt.replace(i, "")
        joined = "{author} on {time}: {txt}".format(author=user_name, time=time_format, txt=txt)
        tweets.append(joined)
    return tweets


if __name__ == "__main__":
    print(get_tweets('GeorgiaTech', 3))

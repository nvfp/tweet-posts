import os
from datetime import datetime

import tweepy


def send_tweet(tweet_content):

    consumer_key = os.environ['TWITTER_API_KEY']
    consumer_secret = os.environ['TWITTER_API_SECRET_KEY']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

    ## Auth
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    ## API
    api = tweepy.API(auth)

    ## Tweet!
    api.update_status(tweet_content)


if __name__ == '__main__':

    dt = datetime.now().strftime('%B %d, %Y, %I:%M %p')
    send_tweet(f'[{dt}] Test tweet from GitHub Actions!')
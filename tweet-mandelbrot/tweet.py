import os
from datetime import datetime

import tweepy


def send_tweet(tweet_content):

    consumer_key = os.environ['TWITTER_API_KEY']
    consumer_secret = os.environ['TWITTER_API_SECRET_KEY']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    response = client.create_tweet(text=tweet_content)
    print(response)
    print(f"https://twitter.com/user/status/{response.data['id']}")


if __name__ == '__main__':

    dt = datetime.now().strftime('%B %d, %Y, %I:%M %p')
    send_tweet(f'[{dt}] Test tweet from GitHub Actions!')
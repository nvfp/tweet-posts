# import logging
import os
from datetime import datetime

import tweepy


# logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S')
# logger = logging.getLogger(__name__)


def send_tweet(tweet_content):
    # logger.info(f'Tweeting {repr(tweet_content)}.')

    consumer_key = os.environ['TWITTER_API_KEY']
    consumer_secret = os.environ['TWITTER_API_SECRET_KEY']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    response = client.create_tweet(text=tweet_content)
    # logger.debug(response)
    # logger.debug(f"https://twitter.com/user/status/{response.data['id']}")

    # logger.debug('Tweeted!')


def send_tweet_with_image(text, image):

    consumer_key = os.environ['TWITTER_API_KEY']
    consumer_secret = os.environ['TWITTER_API_SECRET_KEY']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

    auth = tweepy.OAuth1UserHandler(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )

    api = tweepy.API(auth)

    media = api.media_upload(filename=image)
    print("MEDIA: ", media)

    tweet = api.update_status(status=text, media_ids=[media.media_id_string])
    print("TWEET: ", tweet)


if __name__ == '__main__':

    dt = datetime.now().strftime('%B %d, %Y, %I:%M %p')
    # send_tweet(f'[{dt}] Test tweet from GitHub Actions!')
    
    img = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'foo.jpg')
    send_tweet_with_image(f'test tweet\n{dt}', img)
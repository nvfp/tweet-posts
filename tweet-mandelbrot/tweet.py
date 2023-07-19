# import logging
import json
import os
from datetime import datetime
from requests_oauthlib import OAuth1Session

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

    url_text = 'https://api.twitter.com/1.1/statuses/update.json'
    url_media = 'https://upload.twitter.com/1.1/media/upload.json'
    twitter = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)

    try:
        with open(image, 'rb') as image_file:
            files = {"media": image_file}
            req_media = twitter.post(url_media, files=files)
            req_media.raise_for_status()  # Raise an exception for non-2xx status codes

        media_id = json.loads(req_media.text)['media_id']

        params = {'status': text, "media_ids": [media_id]}
        req_text = twitter.post(url_text, params=params)
        req_text.raise_for_status()  # Raise an exception for non-2xx status codes

        print("Tweet sent successfully.")
    except Exception as e:
        print("An error occurred while sending the tweet: %s", e)
        raise


if __name__ == '__main__':

    dt = datetime.now().strftime('%B %d, %Y, %I:%M %p')
    # send_tweet(f'[{dt}] Test tweet from GitHub Actions!')
    
    img = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'foo.jpg')
    send_tweet_with_image(f'test tweet\n{dt}', img)
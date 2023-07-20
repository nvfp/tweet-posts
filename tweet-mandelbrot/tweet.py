# import logging
import os
import re
from datetime import datetime

import tweepy

from mykit.kit.utils import printer


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
    printer('INFO: Sending tweet.')

    consumer_key = os.environ['TWITTER_API_KEY']
    consumer_secret = os.environ['TWITTER_API_SECRET_KEY']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

    ## ref: https://stackoverflow.com/questions/70891698/how-to-post-a-tweet-with-media-picture-using-twitter-api-v2-and-tweepy-python
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret,)
    client_v1 = tweepy.API(auth)

    client_v2 = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    media = client_v1.media_upload(filename=image)
    media_id = media.media_id

    client_v2.create_tweet(text=text, media_ids=[media_id])



def send_tweet_with_image_then_reply(text, image, reply):
    printer('INFO: Sending tweet.')

    consumer_key = os.environ['TWITTER_API_KEY']
    consumer_secret = os.environ['TWITTER_API_SECRET_KEY']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

    ## ref: https://stackoverflow.com/questions/70891698/how-to-post-a-tweet-with-media-picture-using-twitter-api-v2-and-tweepy-python
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret,)
    client_v1 = tweepy.API(auth)

    client_v2 = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    media = client_v1.media_upload(filename=image)
    media_id = media.media_id

    posted = client_v2.create_tweet(text=text, media_ids=[media_id])

    ## Reply
    tweet_id = posted.data['id']  # Get the id of the tweet
    client_v2.create_tweet(text=reply, in_reply_to_tweet_id=tweet_id)


if __name__ == '__main__':

    # dt = datetime.now().strftime('%B %d, %Y, %I:%M %p')
    # send_tweet(f'[{dt}] Test tweet from GitHub Actions!')

    PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    ## Image path
    IMG = os.path.join(PROJECT_ROOT_DIR, 'drafts', 'result.png')

    ## Metadata file path
    METADATA = [f for f in os.listdir(os.path.join(PROJECT_ROOT_DIR, 'drafts')) if f.endswith('.txt')][0]

    ## Parse some metadata to post
    with open(os.path.join(PROJECT_ROOT_DIR, 'drafts', METADATA), 'r') as f:
        md_text = f.read()
    md_id = re.search(r'id: (?P<id>.*)', md_text).group('id')
    md_xmin = re.search(r'xmin: (?P<xmin>.*)', md_text).group('xmin')
    md_xmax = re.search(r'xmax: (?P<xmax>.*)', md_text).group('xmax')
    md_ymin = re.search(r'ymin: (?P<ymin>.*)', md_text).group('ymin')
    md_ymax = re.search(r'ymax: (?P<ymax>.*)', md_text).group('ymax')
    md_n_iter = re.search(r'n_iter: (?P<n_iter>.*)', md_text).group('n_iter')
    md_antialiasing_is_on = re.search(r'antialiasing_is_on: (?P<antialiasing_is_on>.*)', md_text).group('antialiasing_is_on')

    tweet = (
        f'Happy {datetime.now().strftime("%A")}!    uid-{md_id}'
    )
    reply = (
        '@nvlts metadata:\n'
        f'real:\n{[float(md_xmin), float(md_xmax)]}\n'
        f'imag:\n{[float(md_ymin), float(md_ymax)]}\n'
        f'#iteration: {md_n_iter}\n'
        f'antialiasing: {md_antialiasing_is_on}\n'
        f'archive: https://github.com/nvfp/tweet-posts/blob/main/tweet-mandelbrot/archive/{md_id}.txt'
    )
    send_tweet_with_image_then_reply(tweet, IMG, reply)
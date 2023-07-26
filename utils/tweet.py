import os
import tweepy

from mykit.kit.utils import printer


def tweet(text, image):
    printer('INFO: Sending tweet.')

    consumer_key = os.environ['TWITTER_API_KEY']
    consumer_secret = os.environ['TWITTER_API_SECRET_KEY']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

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

    tweet_id = posted.data['id']  # Get the id of the tweet
    printer(f'INFO: Sent with tweet_id {repr(tweet_id)}.')

    return tweet_id
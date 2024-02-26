import os
import tweepy

def tweet(text, image):
    printer('INFO: Sending tweet.')

    access_token = os.environ['X_ACCESS_TOKEN_SECRET']
    access_token_secret = os.environ['X_ACCESS_TOKEN_SECRET']
    consumer_key = os.environ['X_API_KEY']
    consumer_secret = os.environ['X_API_KEY_SECRET']

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret,)
    client_v1 = tweepy.API(auth)

    client_v2 = tweepy.Client(
        access_token=access_token, access_token_secret=access_token_secret,
        consumer_key=consumer_key, consumer_secret=consumer_secret
    )

    try:
        media = client_v1.media_upload(filename=image)
        media_id = media.media_id

        posted = client_v2.create_tweet(text=text, media_ids=[media_id])

        tweet_id = posted.data['id']  # Get the id of the tweet
        printer(f'INFO: Sent with tweet_id {repr(tweet_id)}.')

        return tweet_id
    except Exception as err:
        printer(f'ERROR: {err}')
        return 'FAIL'
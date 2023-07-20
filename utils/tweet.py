import os

import tweepy

from mykit.kit.utils import printer


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

    posted = client_v2.create_tweet(text=text, media_ids=[media_id])

    tweet_id = posted.data['id']  # Get the id of the tweet
    printer(f'DEBUG: tweet_id: {tweet_id}')

    ## Store the tweet id for future need
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        print(f'tweet_id={tweet_id}', file=f)


def send_tweet_with_image_then_reply(text, image, reply):
    printer('INFO: Sending tweet with reply.')

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
    printer(f'DEBUG: tweet_id: {tweet_id}')
    client_v2.create_tweet(text=reply, in_reply_to_tweet_id=tweet_id)
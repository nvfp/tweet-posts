import os, requests, tweepy, random, json, datetime
from .shared import RENDERED_IMG_PTH

def uploadTwitter(imgPath, postDesc):
    access_token = os.environ['X_ACCESS_TOKEN']
    access_token_secret = os.environ['X_ACCESS_TOKEN_SECRET']
    consumer_key = os.environ['X_API_KEY']
    consumer_secret = os.environ['X_API_KEY_SECRET']

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)  # the v1.X version of API for image uploading, because API ver 2 somehow doesnt support image-uploading.
    auth.set_access_token(access_token, access_token_secret,)
    client_v1 = tweepy.API(auth)

    client_v2 = tweepy.Client(  # the API version 2 for the texts, im not sure, but as far as i know, the free plan only supports version 2 for tweeting text.
        access_token=access_token, access_token_secret=access_token_secret,
        consumer_key=consumer_key, consumer_secret=consumer_secret
    )

    media = client_v1.media_upload(filename=imgPath)  # post the image first then the desc
    client_v2.create_tweet(text=postDesc, media_ids=[media.media_id])  # Upload the post's description

    print('uploaded to twitter.')

def uploadMastodon(imgPath, postDesc):
    access_token = os.environ['MASTODON_ACCESS_TOKEN']

    with open(imgPath, 'rb') as file:  # uploading the image first
        response = requests.post(
            'https://mastodon.social/api/v2/media',
            headers={'Authorization': f'Bearer {access_token}'},
            files={'file': file}
        )
        if response.status_code != 200:raise AssertionError(f"image response: {response}")

    payload = {'status': postDesc, 'media_ids[]': response.json()['id']}  # now, upload the post's description
    response = requests.post(
        'https://mastodon.social/api/v1/statuses',
        headers={'Authorization': f'Bearer {access_token}'},
        data=payload
    )
    if response.status_code != 200:raise AssertionError(f"text response: {response}")

    print('uploaded to mastodon.')

def upload():
    pth = RENDERED_IMG_PTH
    desc=f"Happy {datetime.datetime.now().strftime('%A')}!"
    uploadTwitter(pth, desc)
    uploadMastodon(pth, desc)

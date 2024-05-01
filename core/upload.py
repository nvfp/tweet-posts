import os, requests, tweepy, random, json, datetime

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
    try:
        media = client_v1.media_upload(filename=imgPath)  # post the image first
        media_id = media.media_id

        posted = client_v2.create_tweet(text=postDesc, media_ids=[media_id])  # the the text (post description)

        tweet_id = posted.data['id']
        print(f"tweet_id: {tweet_id}")
        return tweet_id
    except Exception as err:
        print(f'ERROR: {err}')
        return f"Err: {err}"

def uploadMastodon(imgPath, postDesc):
    access_token = os.environ['MASTODON_ACCESS_TOKEN']

    ## Image
    with open(imgPath, 'rb') as file:
        response = requests.post(
            'https://mastodon.social/api/v2/media',
            headers={'Authorization': f'Bearer {access_token}'},
            files={'file': file}
        )
        if response.status_code != 200:
            print(f'WARNING: image response: {response}')
            return f"Err: {response}"
    media_id = response.json()['id']

    ## Text
    payload = {'status': postDesc, 'media_ids[]': media_id}
    response = requests.post(
        'https://mastodon.social/api/v1/statuses',
        headers={'Authorization': f'Bearer {access_token}'},
        data=payload
    )
    # print(json.dumps(response.json(), indent=4))
    if response.status_code != 200:
        print(f'WARNING: text response: {response}')
        return f"Err: {response}"
    post_id = response.json()['id']
    print(f'INFO: Sent. post_id: {repr(post_id)}')
    return post_id

def upload():
    pth='./the_rendered_image.jpg'
    desc=f"Happy {datetime.datetime.now().strftime('%A')}!"
    uploadTwitter(pth, desc)
    uploadMastodon(pth, desc)

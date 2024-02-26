import os, requests, tweepy, random
from datetime import datetime
from .shared import RENDERED_IMG_PTH

def post_twitter(post_desc, image_pth):  # post_desc: the caption; image_pth: the full path to the image
    print('INFO: Sending tweet.')

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
        media = client_v1.media_upload(filename=image_pth)
        media_id = media.media_id

        posted = client_v2.create_tweet(text=post_desc, media_ids=[media_id])

        tweet_id = posted.data['id']  # Get the id of the tweet
        print(f'INFO: Sent with tweet_id {repr(tweet_id)}.')

        return tweet_id
    except Exception as err:
        print(f'ERROR: {err}')
        return 'FAIL'

def post_masto(post_desc, image_pth):
    print('INFO: Sending to Mastodon.')
    access_token = os.environ['MASTODON_ACCESS_TOKEN']

    ## Image
    with open(image_pth, 'rb') as file:
        response = requests.post(
            'https://mastodon.social/api/v2/media',
            headers={'Authorization': f'Bearer {access_token}'},
            files={'file': file}
        )
        if response.status_code != 200:
            print(f'WARNING: image response: {response}')
            return 'FAIL'
    media_id = response.json()['id']

    ## Text
    payload = {'status': post_desc, 'media_ids[]': media_id}
    response = requests.post(
        'https://mastodon.social/api/v1/statuses',
        headers={'Authorization': f'Bearer {access_token}'},
        data=payload
    )
    if response.status_code != 200:
        print(f'WARNING: text response: {response}')
        return 'FAIL'
    # printer(json.dumps(response.json(), indent=4))
    post_id = response.json()['id']
    print(f'INFO: Sent. post_id: {repr(post_id)}')
    return post_id

def get_post_desc(fractal_name):
    def get_msg():
        day = datetime.now().strftime('%A')
        msgs = [
            f'Happy {day}!',
            f'How\'s your day?',
            f'Enjoy your {day}!',
            f'{day} vibes!',
            f'Have an awesome {day}!',
            f'Wishing you a fantastic day!',
            f'Hey there, it\'s {day}!',
            f'Let\'s rock this {day}!',
            f'Having a blast on {day}?',
            f'Wishing you a rad {day}!',
            f'Hope you\'re having a great {day}!',
            f'Smile, it\'s {day}!',
            f'Keep shining on {day}!',
            f'Let\'s make it a memorable {day}!',
            f'Cheers to an incredible {day}!',
            f'Hope your {day} is awesome!',
            f'Sending you this fractal on this {day}!',
            f'Let the magic of {day} fill your heart!',
            f'You rock, and so does this {day}!',
            f'Shine bright like the sun on this {day}!',
            f'Wishing you a wonderful {day}!',
            f'Let this {fractal_name} inspire your {day}.',
            f'Happy {day}! Enjoy the beauty of {fractal_name}.',
            f'Warm wishes for your {day}, and let\'s have a look at this {fractal_name}.',
            f'{fractal_name} vibes to brighten your {day}.',
            f'Ever heard of this {fractal_name}?',
            f'Surprise! It\'s a {fractal_name}!',
            f'Good {day}! This {fractal_name} is for you!',
            f'Wishing you a joyful day!',
            f'Another {day}, another {fractal_name}!',
            f'Feeling the {fractal_name} vibes today!',
            f'Smile on this lovely day!',
            f'Guess what? It\'s {fractal_name}!',
            f'Have a great day!',
            f'Feeling good today!',
            f'Wishing you the best!',
            f'Cheers to an incredible {day}! You got this!',
            f'Keep smiling!',
            f'Smile!',
            f'Chin up, lovely humans!',
            f'Have an awesome day!',
            f'Let this {fractal_name} brighten up your {day}!',
            f'Cheers to a fantastic {day}!',
            f'Hope you have an amazing {day}!',
            f'Chin up, buttercup!',
            f'Today is awesome!',
            f'Surprise! {fractal_name}!',
            f'Have an extraordinary {day}!',
            f'Brighten your {day}!',
            f'Hello {day}! This {fractal_name} is yours!',
            f"Hey wait, look! it's {fractal_name}!",
            f"Wow, take a look! There's {fractal_name}!",
            f"Look what we have here! it's {fractal_name}!",
            f"Wow, guess what? it's {fractal_name}!",
            f"Look closely, it's {fractal_name}!",
            f"Beautiful {day} with this {fractal_name}!",
            f"This {day} is made even better by this {fractal_name}!",
            f"Enjoying the {day} with this {fractal_name}.",
            f"A great {day} and a beautiful {fractal_name}.",
            f"{day} is shining brightly, just like this {fractal_name}.",
            f"You are lovely!",
            f"How was your day?",
            f"you are awesome.",
            f"you are cool",
            f"you are fantastic!",
            f"you're awesome!",
        ]
        if len(msgs) != len(set(msgs)): raise AssertionError(f"Contains duplicate msgs.")
        return random.choice(msgs)
    msg = get_msg()

    def get_tags():
        tags = [
            '#AI',
            '#MachineLearning',
            '#DeepLearning',
            '#Mathematics',
            '#Nature',
            '#Fractals',
            '#Art',
            '#DigitalArt',
            '#VisualArt',
            "#GenerativeArt",
        ]
        if len(tags) != len(set(tags)): raise AssertionError("duplicated")
        out = []
        while len(out) != 2:  # EDITME
            t = random.choice(tags)
            if t in out: continue  # no duplicate
            out.append(t)
        return ' '.join(out)
    tags = get_tags()

    return f"{msg} {tags}"

def post_online(fractal_name):
    post_desc = get_post_desc(fractal_name)

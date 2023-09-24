import os
import praw

from mykit.kit.utils import printer


def post_to_subreddit(text, image_abs_path):

    r = praw.Reddit(
        client_id=os.environ['REDDIT_ID'],
        client_secret=os.environ['REDDIT_SECRET'],
        username=os.environ['REDDIT_USERNAME'],
        password=os.environ['REDDIT_PASSWORD'],
        user_agent='post-to-subreddit_tweet-posts',
    )

    try:
        submission = r.subreddit('hourly_fractals').submit_image(text, image_abs_path)
        x = submission.url
        print('---------------')
        print(x)
        print('---------------')
        print(repr(x))
        print('---------------')
        return '<BETA>'
    except Exception as err:
        printer(f'ERROR: {err}')
        return 'FAIL'

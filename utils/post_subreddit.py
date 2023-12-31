import os
# import praw

from mykit.kit.utils import printer


def post_to_subreddit(text, image_abs_path):

    ## Disable Reddit posts since Reddit keeps blocking my subreddit
    return f"Not uploaded, but here's the text: {text}"

    printer('INFO: sending to Reddit...')

    r = praw.Reddit(
        client_id=os.environ['REDDIT_ID'],
        client_secret=os.environ['REDDIT_SECRET'],
        username=os.environ['REDDIT_USERNAME'],
        password=os.environ['REDDIT_PASSWORD'],
        user_agent='post-to-subreddit_tweet-posts',
    )

    try:
        submission = r.subreddit('hourly_fractals').submit_image(text, image_abs_path)

        # print(f'submission.author: {repr(submission.author)}.')
        # print(f'submission.url: {repr(submission.url)}.')
        # print(f'submission.id: {repr(submission.id)}.')
        # print(f'submission.permalink: {repr(submission.permalink)}.')

        ## I have no idea why Reddit posts need to be approved so people can see them.
        ## TODO: can we just set auto-approve rather than doing this?
        submission.mod.approve()

        the_id = submission.permalink
        printer(f'INFO: done, sent. subreddit with the_id: {repr(the_id)}.')

        return the_id
    except Exception as err:
        printer(f'ERROR: {err}')
        return 'FAIL'

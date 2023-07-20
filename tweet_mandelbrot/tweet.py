import os
import random
import re
import sys
from datetime import datetime

from mykit.kit.utils import printer

## Make all folders under repo root directory importable
_REPO_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
printer(f'DEBUG: Appending {repr(_REPO_ROOT_DIR)} to `sys.path`.')
sys.path.append(_REPO_ROOT_DIR)

from utils.tweet import send_tweet_with_image_then_reply
from tweet_mandelbrot.constants import DRAFT_DIR


if __name__ == '__main__':

    ## Image path
    IMG = os.path.join(DRAFT_DIR, 'result.png')

    ## Metadata
    md_file_name = [f for f in os.listdir(DRAFT_DIR) if f.endswith('.txt')][0]
    md_file_path = os.path.join(DRAFT_DIR, md_file_name)

    ## Parse some metadata to post
    with open(md_file_path, 'r') as f:
        md_text = f.read()
    md_id = re.search(r'id: (?P<id>.*)', md_text).group('id')
    md_xmin = re.search(r'xmin: (?P<xmin>.*)', md_text).group('xmin')
    md_xmax = re.search(r'xmax: (?P<xmax>.*)', md_text).group('xmax')
    md_ymin = re.search(r'ymin: (?P<ymin>.*)', md_text).group('ymin')
    md_ymax = re.search(r'ymax: (?P<ymax>.*)', md_text).group('ymax')
    md_n_iter = re.search(r'n_iter: (?P<n_iter>.*)', md_text).group('n_iter')
    md_antialiasing_is_on = re.search(r'antialiasing_is_on    : (?P<antialiasing_is_on>.*)', md_text).group('antialiasing_is_on')

    ## Tweeting
    day = datetime.now().strftime('%A')
    random_greet = [
        f'Happy {day}!',
        f'How\'s your {day}?',
        f'Enjoy your {day}!',
        f'{day} vibes!',
        f'Have an awesome {day}!',
        f'Wishing you a fantastic {day}!',
        f'Hey there, it\'s {day}!',
        f'Let\'s rock this {day}!',
        f'Having a blast on {day}?',
        f'Wishing you a rad {day}!',
    ]
    tweet = (
        f'{random.choice(random_greet)} — image id: {md_id}'
    )
    reply = (
        '@nvfastplease\n'
        'metadata:\n'
        f'real:\n{[float(md_xmin), float(md_xmax)]}\n'
        f'imag:\n{[float(md_ymin), float(md_ymax)]}\n'
        f'#iteration: {md_n_iter}\n'
        f'antialiasing: {md_antialiasing_is_on}\n'
        f'archive: https://github.com/nvfp/tweet-posts/blob/main/tweet_mandelbrot/archive/{md_id}.txt'
    )
    send_tweet_with_image_then_reply(tweet, IMG, reply)
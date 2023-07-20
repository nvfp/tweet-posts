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

from utils.tweet import send_tweet_with_image
from tweet_mandelbrot.constants import DRAFT_DIR


if __name__ == '__main__':

    ## Image path
    IMG = os.path.join(DRAFT_DIR, 'result.png')

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
        f'Hope you\'re having a great {day}!',
        f'Smile, it\'s {day}!',
        f'Keep shining on {day}!',
        f'Let\'s make it a memorable {day}!',
        f'Cheers to an incredible {day}!',
        f'Hope your {day} is awesome!',
        f'Sending you good vibes on this {day}!',
        f'Let the magic of {day} fill your heart!',
        f'You rock, and so does this {day}!',
        f'Shine bright like the sun on this {day}!',
        f'Wishing you a wonderful {day}!',
    ]
    tweet = random.choice(random_greet)
    send_tweet_with_image(tweet, IMG)
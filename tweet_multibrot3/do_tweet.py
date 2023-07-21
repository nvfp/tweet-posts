import os
import sys
from datetime import datetime

from mykit.kit.utils import printer

## Make all folders under repo root directory importable
_REPO_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
printer(f'DEBUG: Appending {repr(_REPO_ROOT_DIR)} to `sys.path`.')
sys.path.append(_REPO_ROOT_DIR)

from utils.get_random_fractal_greeting import get_random_fractal_greeting
from utils.tweet import send_tweet_with_image
from tweet_multibrot3.constants import DRAFT_DIR


if __name__ == '__main__':

    ## Image path
    IMG = os.path.join(DRAFT_DIR, 'result.png')

    ## Tweeting
    fractal = 'Multibrot'
    day = datetime.now().strftime('%A')
    
    tweet = get_random_fractal_greeting(day, fractal)
    send_tweet_with_image(tweet, IMG)
from datetime import datetime

from utils.get_random_fractal_greeting import get_random_fractal_greeting
from utils.get_random_hashtag import get_random_hashtag


NUM_HASHTAGS = 3


def get_text(fractal):
    day = datetime.now().strftime('%A')
    greet = get_random_fractal_greeting(day, fractal)
    hashtags = get_random_hashtag(NUM_HASHTAGS)
    return f'{greet}  {" ".join(hashtags)}'

import random


def _get_list(day, fractal):
    """Testing purposes"""
    random_greetings = [
        f'Happy {day}!',
        f'How\'s your day?',  # yes, it's "day", not `{day}`
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
        f'Let this {fractal} inspire your {day}.',
        f'Happy {day}! Enjoy the beauty of {fractal}.',
        f'Warm wishes for your {day}, and let\'s have a look at this {fractal}.',
        f'{fractal} vibes to brighten your {day}.',
        f'Ever heard of this {fractal}?',
        f'Surprise! It\'s a {fractal}!',
        f'Good {day}! This {fractal} is for you!',
        f'Wishing you a joyful day!',
        f'Another {day}, another {fractal}!',
        f'Feeling the {fractal} vibes today!',
        f'Smile on this lovely day!',
        f'Guess what? It\'s {fractal}!',
        f'Have a great day!',
        f'Feeling good today!',
        f'Wishing you the best!',
        f'Cheers to an incredible {day}! You got this!',
        f'Keep smiling!',
        f'Smile!',
        f'Chin up, lovely humans!',
        f'Have an awesome day!',
        f'Let this {fractal} brighten up your {day}!',
        f'Cheers to a fantastic {day}!',
        f'Hope you have an amazing {day}!',
        f'Chin up, buttercup!',
        f'Today is awesome!',
        f'Surprise! {fractal}!',
        f'Have an extraordinary {day}!',
        f'Brighten your {day}!',
        f'Hello {day}! This {fractal} is yours!',
    ]
    return random_greetings


def get_random_fractal_greeting(day, fractal):
    random_greetings = _get_list(day, fractal)
    return random.choice(random_greetings)
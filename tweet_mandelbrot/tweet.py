import os
import re
from datetime import datetime

from utils.constants import PROJECT_ROOT_DIR
from utils.tweet import send_tweet_with_image_then_reply


DRAFT_DIR = os.path.join(PROJECT_ROOT_DIR, 'tweet-mandelbrot', 'drafts')


if __name__ == '__main__':

    ## Image path
    IMG = os.path.join(DRAFT_DIR, 'result.png')

    ## Metadata file path
    METADATA = [f for f in os.listdir(DRAFT_DIR) if f.endswith('.txt')][0]

    ## Parse some metadata to post
    with open(os.path.join(DRAFT_DIR, METADATA), 'r') as f:
        md_text = f.read()
    md_id = re.search(r'id: (?P<id>.*)', md_text).group('id')
    md_xmin = re.search(r'xmin: (?P<xmin>.*)', md_text).group('xmin')
    md_xmax = re.search(r'xmax: (?P<xmax>.*)', md_text).group('xmax')
    md_ymin = re.search(r'ymin: (?P<ymin>.*)', md_text).group('ymin')
    md_ymax = re.search(r'ymax: (?P<ymax>.*)', md_text).group('ymax')
    md_n_iter = re.search(r'n_iter: (?P<n_iter>.*)', md_text).group('n_iter')
    md_antialiasing_is_on = re.search(r'antialiasing_is_on    : (?P<antialiasing_is_on>.*)', md_text).group('antialiasing_is_on')

    tweet = (
        f'Happy {datetime.now().strftime("%A")}!    uid-{md_id}'
    )
    reply = (
        '@nvlts metadata:\n'
        f'real:\n{[float(md_xmin), float(md_xmax)]}\n'
        f'imag:\n{[float(md_ymin), float(md_ymax)]}\n'
        f'#iteration: {md_n_iter}\n'
        f'antialiasing: {md_antialiasing_is_on}\n'
        f'archive: https://github.com/nvfp/tweet-posts/blob/main/tweet-mandelbrot/archive/{md_id}.txt'
    )
    send_tweet_with_image_then_reply(tweet, IMG, reply)
import numpy as np
import os
import random
import sys
import time
from datetime import datetime

from mykit.kit.utils import printer

## Make all folders under repo root directory importable
_REPO_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
printer(f'DEBUG: Appending {repr(_REPO_ROOT_DIR)} to `sys.path`.')
sys.path.append(_REPO_ROOT_DIR)

from utils.constants import __version__, ARCHIVE_TEMP_DIR
from utils.get_text import get_text
from utils.get_ppm import get_ppm
from utils.save_img import save_img
from utils.tweet import tweet
from utils.post_mastodon import post_mastodon
from utils.post_subreddit import post_to_subreddit
from tweet_mandelbrot.get_raw import get_raw_grayscale_image
from tweet_mandelbrot.write_metadata import write_metadata


IMAGE_PTH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'the-result.png')
printer(f'DEBUG: IMAGE_PTH: {repr(IMAGE_PTH)}.')


def get_random_range():

    ## The region where the fractal is visible
    x_bound_min = -2.75
    x_bound_max = 1.25
    y_bound_min = -1.124
    # y_bound_max = 1.124
    y_bound_max = 1.13  # to compensate the aspect ratio ((x_bound_max-x_bound_min)*9/16)

    total_width = x_bound_max - x_bound_min
    # total_height = y_bound_max - y_bound_min

    ## The captured one
    frame_width = total_width/random.randint(1, 10000)
    frame_height = frame_width*(9/16)  # 16:9 aspect ratio

    xmin = random.uniform(x_bound_min, x_bound_max-frame_width)
    xmax = xmin + frame_width

    ymin = random.uniform(y_bound_min, y_bound_max-frame_height)
    ymax = ymin + frame_height

    return xmin, xmax, ymin, ymax


if __name__ == '__main__':

    n_iter = random.randint(128, 1024)
    ct = random.randint(1, 255)  # PPM color threshold
    hue_offset = random.randint(0, 359)
    saturation = round( random.uniform(-1, 1), 2 )

    ## Don't capture blank image
    num_attempts = 0
    dur_t0 = time.time()
    std = 0  # standard deviation
    while std < 15:  # This essentially checks the noise of the image (if 0 -> all uniform, aka a blank image)
        num_attempts += 1
        if (time.time() - dur_t0) > 850: break  # Guard
        xmin, xmax, ymin, ymax = get_random_range()
        ## Render
        raw = get_raw_grayscale_image(1280, 720, True, 2, n_iter, xmin, xmax, ymin, ymax)
        std = np.std(raw)
    dur = time.time() - dur_t0
    printer(f'INFO: std: {std}  dur: {dur}  num_attempts: {num_attempts}')

    ppm_data = get_ppm(raw, 1280, 720, ct, hue_offset, saturation)

    ## Random FFmpeg filters
    edit_contrast   = round( random.uniform(0.7, 1.8)  , 2 )
    edit_brightness = round( random.uniform(-0.1, 0.23), 2 )
    edit_saturation = round( random.uniform(0.25, 1.75), 2 )
    edit_gamma      = round( random.uniform(0.9, 1.1)  , 2 )
    edit_gamma_r    = round( random.uniform(0.9, 1.1)  , 2 )
    edit_gamma_g    = round( random.uniform(0.9, 1.1)  , 2 )
    edit_gamma_b    = round( random.uniform(0.9, 1.1)  , 2 )
    edit_vignette   = random.randint(-48, 33)
    edit_temp       = random.randint(2000, 8000)

    # Export
    file_size = save_img(
        IMAGE_PTH,
        ppm_data,

        edit_contrast,
        edit_brightness,
        edit_saturation,
        edit_gamma,
        edit_gamma_r,
        edit_gamma_g,
        edit_gamma_b,
        edit_vignette,
        edit_temp
    )

    ## Posting
    text = get_text('Mandelbrot Set')
    tweet_id = tweet(text, IMAGE_PTH)
    masto_id = post_mastodon(text, IMAGE_PTH)
    subre_id = post_to_subreddit(text, IMAGE_PTH)  # post's permalink

    ## Metadata
    if os.path.exists(ARCHIVE_TEMP_DIR): raise AssertionError(f'Already exists: {repr(ARCHIVE_TEMP_DIR)}.')
    os.mkdir(ARCHIVE_TEMP_DIR)
    write_metadata(
        os.path.join(ARCHIVE_TEMP_DIR, f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_Mandelbrot_{tweet_id}_{__version__}.txt'),
        tweet_id, masto_id, subre_id,

        n_iter,
        ct,
        hue_offset,
        saturation,

        num_attempts, int(dur), round(std, 2), file_size,

        xmin, xmax, ymin, ymax,

        edit_contrast,
        edit_brightness,
        edit_saturation,
        edit_gamma,
        edit_gamma_r,
        edit_gamma_g,
        edit_gamma_b,
        edit_vignette,
        edit_temp,
    )

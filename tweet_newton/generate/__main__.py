import numpy as np
import os
import random
import time
import sys

from mykit.kit.utils import printer

## Make all folders under repo root directory importable
_REPO_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
printer(f'DEBUG: Appending {repr(_REPO_ROOT_DIR)} to `sys.path`.')
sys.path.append(_REPO_ROOT_DIR)

from utils.constants import FFMPEG
from tweet_newton.constants import DRAFT_DIR
from tweet_newton.generate.get_ppm import get_raw_grayscale_image, get_ppm
from tweet_newton.generate.save_img import save_img
from tweet_newton.generate.write_metadata import write_metadata


def get_random_range():

    ## The region where the fractal is visible
    x_bound_min = -3
    x_bound_max = 3
    y_bound_min = -2
    y_bound_max = 2

    total_width = x_bound_max - x_bound_min
    total_height = y_bound_max - y_bound_min

    ## The captured one
    frame_width = total_width/random.randint(1, 100)
    frame_height = frame_width*(9/16)  # 16:9 aspect ratio

    xmin = random.uniform(x_bound_min, x_bound_max-frame_width)
    xmax = xmin + frame_width

    ymin = random.uniform(y_bound_min, y_bound_max-frame_height)
    ymax = ymin + frame_height

    return xmin, xmax, ymin, ymax, frame_width, frame_height


def main():

    w, h = 1920, 1080  # should 16:9 AR. Note: FHD could take so long to be done
    # w, h = 1280, 720

    antialiasing_is_on = random.choice([True, False])
    antialiasing_supsample = 2

    n_iter = random.randint(32, 128)
    ct = random.randint(1, 255)
    hue_offset = random.randint(0, 359)
    saturation = random.uniform(-1, 1)

    ## Don't capture blank image
    num_attempts = 0
    dur_t0 = time.time()
    std = 0  # standard deviation
    while std < 5:  # This essentially checks the noise of the image (if 0 -> all uniform, aka a blank image)
        num_attempts += 1
        if (time.time() - dur_t0) > 1200: break  # Guard
        xmin, xmax, ymin, ymax, frame_width, frame_height = get_random_range()
        ## Render
        raw = get_raw_grayscale_image(
            w, h,
            antialiasing_is_on,
            antialiasing_supsample,
            n_iter,
            xmin, xmax,
            ymin, ymax
        )
        std = np.std(raw)
    dur = time.time() - dur_t0
    printer(f'INFO: std: {std}  dur: {dur}  num_attempts: {num_attempts}')

    ppm_data = get_ppm(
        raw,
        w, h, ct,
        hue_offset, saturation
    )

    ## Random FFmpeg filters
    edit_contrast   = random.uniform(0.7, 1.8)
    edit_brightness = random.uniform(-0.1, 0.23)
    edit_saturation = random.uniform(0.25, 1.75)
    edit_gamma      = random.uniform(0.9, 1.1)
    edit_gamma_r    = random.uniform(0.9, 1.1)
    edit_gamma_g    = random.uniform(0.9, 1.1)
    edit_gamma_b    = random.uniform(0.9, 1.1)
    edit_vignette   = random.randint(-48, 33)
    edit_temp       = random.randint(2000, 8000)

    # Export
    file_size = save_img(
        FFMPEG,
        os.path.join(DRAFT_DIR, 'result.png'),
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

    write_metadata(
        os.path.join(DRAFT_DIR, 'metadata.txt'),
        w, h,

        antialiasing_is_on, antialiasing_supsample,

        n_iter,
        ct,
        hue_offset,
        saturation,

        num_attempts, dur, std,
        file_size,

        xmin, xmax, ymin, ymax, frame_width, frame_height,

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


if __name__ == '__main__':
    main()
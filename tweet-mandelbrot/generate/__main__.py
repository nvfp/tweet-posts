import numpy as np
import os
import random
import sys
import time

from mykit.kit.utils import printer

PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
printer(f'DEBUG: Appending {repr(PROJECT_ROOT_DIR)} to `sys.path`.')
sys.path.append(PROJECT_ROOT_DIR)
from generate.get_ppm import get_raw_grayscale_image, get_ppm
from generate.save_img import save_img
from generate.write_metadata import write_metadata


def get_random_range():

    ## The region where the Mandelbrot set is visible
    x_bound_min = -2.75
    x_bound_max = 1.25
    y_bound_min = -1.124
    y_bound_max = 1.124

    total_width = x_bound_max - x_bound_min
    total_height = y_bound_max - y_bound_min

    ## The captured one
    frame_width = total_width/random.randint(1, 10000)
    frame_height = frame_width*(9/16)  # 16:9 aspect ratio

    xmin = random.uniform(x_bound_min, x_bound_max-frame_width)
    xmax = xmin + frame_width

    ymin = random.uniform(y_bound_min, y_bound_max-frame_height)
    ymax = ymin + frame_height

    return xmin, xmax, ymin, ymax, frame_width, frame_height


def main():

    w, h = 960, 540

    ## Mandelbrot set config
    antialiasing_is_on = False
    antialiasing_supsample = random.randint(2, 3)

    # use_fast_renderer = random.choice([True, False])
    use_fast_renderer = True  # Note: Using the fast renderer disables the use of the 'degree' and 'r_conv' options
    n_iter = random.randint(64, 256)
    degree = 2
    r_conv = 2
    is_grayscale = random.choice([True, False])
    ct = random.randint(1, 255)
    hue_offset = random.randint(0, 359)
    saturation = random.uniform(-1, 1)

    ## Don't capture blank image
    num_attempts = 0
    dur_t0 = time.time()
    std = 0  # standard deviation
    while std < 100:  # This essentially checks the noise of the image (if 0 -> all uniform, aka a blank image)
        num_attempts += 1
        if (time.time() - dur_t0) > 600: break  # Guard
        if (int(time.time() - dur_t0) % 10) == 0: printer(f'INFO: num_attempts: {num_attempts}')
        xmin, xmax, ymin, ymax, frame_width, frame_height = get_random_range()
        ## Render
        raw = get_raw_grayscale_image(
            use_fast_renderer,
            w, h,
            antialiasing_is_on,
            antialiasing_supsample,
            n_iter,
            degree,
            r_conv,
            xmin, xmax,
            ymin, ymax
        )
        std = np.std(raw)
    dur = time.time() - dur_t0
    printer(f'INFO: std: {std}')

    ppm_data = get_ppm(
        raw,
        is_grayscale,
        w, h, ct,
        hue_offset, saturation
    )

    ## Random FFmpeg filters
    edit_contrast   = random.uniform(0.6, 1.4)
    edit_brightness = random.uniform(-0.3, 0.3)
    edit_saturation = random.uniform(0.25, 1.75)
    edit_gamma      = random.uniform(0.7, 1.3)
    edit_gamma_r    = random.uniform(0.7, 1.3)
    edit_gamma_g    = random.uniform(0.7, 1.3)
    edit_gamma_b    = random.uniform(0.7, 1.3)
    edit_vignette   = random.randint(-51, 51)
    edit_temp       = random.randint(2000, 8000)

    # Export
    file_size = save_img(
        'ffmpeg',
        os.path.join(PROJECT_ROOT_DIR, 'drafts', 'result.png'),
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
        w, h,

        antialiasing_is_on, antialiasing_supsample,

        use_fast_renderer,
        n_iter,
        degree,
        r_conv,
        is_grayscale,
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
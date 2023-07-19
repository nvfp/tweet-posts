import os
import random

from .get_ppm import get_raw_grayscale_image, get_ppm
from .save_img import save_img


def main():

    w, h = 1280, 720
    antialiasing_is_on = True
    antialiasing_supsample = 2

    ## Random Mandelbrot set config
    use_fast_renderer = random.choice([True, False])
    n_iter = 200
    degree = 2
    r_conv = 2
    xmin = -2.75
    xmax = 1.25
    ymin = -1.1
    ymax = 1.1
    is_grayscale = False
    ct = 200
    hue_offset = 0
    saturation = 1

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
    ppm_data = get_ppm(
        raw,
        is_grayscale,
        w, h, ct,
        hue_offset, saturation
    )

    ## Random FFmpeg filters
    edit_contrast   = random.uniform(-5, 5)
    edit_brightness = random.uniform(-1, 1)
    edit_saturation = random.uniform(0, 3)
    edit_gamma      = random.uniform(0.1, 3)
    edit_gamma_r    = random.uniform(0.1, 3)
    edit_gamma_g    = random.uniform(0.1, 3)
    edit_gamma_b    = random.uniform(0.1, 3)
    edit_vignette   = random.randint(-90, 90)
    edit_temp       = random.randint(1000, 20000)

    ffmpeg_bin = 'ffmpeg'
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'foo.png')

    # Export
    save_img(
        ffmpeg_bin, file_path, ppm_data,

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


if __name__ == '__main__':
    main()
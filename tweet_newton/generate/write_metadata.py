import time
from datetime import datetime

from mykit.kit.text import byteFmt
from mykit.kit.utils import printer


def get_text(
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
):
    return f"""
Image metadata
==============

type: Phoenix
date: {datetime.now().strftime('%B %d, %Y, %A %I:%M %p')}
timestamp: {time.time()}

resolution: {w}x{h}

antialiasing_is_on    : {antialiasing_is_on}
antialiasing_supsample: {antialiasing_supsample}

n_iter: {n_iter}
ct: {ct}
hue_offset: {hue_offset}
saturation: {saturation}

num_attempts: {num_attempts}
dur: {dur}
std: {std}
size: {file_size} ({byteFmt(file_size)})

xmin: {xmin}
xmax: {xmax}
ymin: {ymin}
ymax: {ymax}
frame_width: {frame_width}
frame_height: {frame_height}

edit_contrast: {edit_contrast}
edit_brightness: {edit_brightness}
edit_saturation: {edit_saturation}
edit_gamma: {edit_gamma}
edit_gamma_r: {edit_gamma_r}
edit_gamma_g: {edit_gamma_g}
edit_gamma_b: {edit_gamma_b}
edit_vignette: {edit_vignette}
edit_temp: {edit_temp}

tweet_id: TWEET_ID
"""


def write_metadata(
    file_path,
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
):
    printer('DEBUG: Writing metadata file.')

    text = get_text(
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
    with open(file_path, 'w') as f:
        f.write(text)
    
    printer(f'INFO: Done, metadata file created at {repr(file_path)}.')
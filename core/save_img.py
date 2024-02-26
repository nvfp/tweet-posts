import os, subprocess as sp
from .shared import FFMPEG, RENDERED_IMG_PTH

def render_fractal_img(
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
):
    filter = (
        'eq='
        f'contrast={edit_contrast}'
        f':brightness={edit_brightness}'
        f':saturation={edit_saturation}'
        f':gamma={edit_gamma}'
        f':gamma_r={edit_gamma_r}'
        f':gamma_g={edit_gamma_g}'
        f':gamma_b={edit_gamma_b}'
        
        ', vignette='
        f'a={abs(edit_vignette)}*PI/180'
        f": mode={'backward' if (edit_vignette > 0) else 'forward'}"
        
        ', colortemperature='
        f'temperature={edit_temp}'
    )
    cmd = [
        FFMPEG,
        '-v', 'error',
        '-f', 'image2pipe',
        '-vcodec', 'ppm',
        '-pix_fmt', 'rgb24',
        '-i', '-',
        '-vf', filter,
        '-q:v', '1',
        RENDERED_IMG_PTH
    ]
    if os.path.exists(RENDERED_IMG_PTH): raise AssertionError
    pipe = sp.Popen(cmd, stdin=sp.PIPE)
    pipe.stdin.write(ppm_data)
    pipe.stdin.close()
    pipe.wait()
    pipe.terminate()

    # file_size = os.path.getsize(file_path)
    # return file_size  # metadata purposes

def render_with_stats():
    pass

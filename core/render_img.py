import subprocess as sp, os
from .shared import RENDERED_IMG_PTH

def saveImg(
    edit_contrast,
    edit_brightness,
    edit_saturation,
    edit_gamma,
    edit_gamma_r,
    edit_gamma_g,
    edit_gamma_b,
    edit_vignette,
    edit_temp,

    ppm_data,
):
    vFilter = (
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
    pipe = sp.Popen([
        'ffmpeg', '-v', 'error',
        '-f', 'image2pipe', '-vcodec', 'ppm', '-pix_fmt', 'rgb24',
        '-i', '-',
        '-vf', vFilter,
        '-q:v', '1',
        RENDERED_IMG_PTH
    ], stdin=sp.PIPE)
    pipe.stdin.write(ppm_data)
    pipe.stdin.close()
    pipe.wait()
    pipe.terminate()

    print(f"Image saved at {repr(RENDERED_IMG_PTH)} ({round(os.path.getsize(RENDERED_IMG_PTH)/1000,1)} kB).")
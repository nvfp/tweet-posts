import os
import subprocess as sp


def save_img(
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
):
    print(f'DEBUG: Attempting to save the image to {repr(file_path)}.')

    ## Check
    if os.path.exists(file_path):
        raise FileExistsError(f'File already exists: {repr(file_path)}.')

    if edit_vignette > 0:
        vig_mode = 'backward'
    else:
        vig_mode = 'forward'

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
        f': mode={vig_mode}'
        
        ', colortemperature='
        f'temperature={edit_temp}'
    )

    pipe = sp.Popen(
        [
            ffmpeg_bin,
            '-v', 'error',
            '-f', 'image2pipe',
            '-vcodec', 'ppm',
            '-pix_fmt', 'rgb24',
            '-i', '-',
            '-vf', filter,
            file_path
        ],
        stdin=sp.PIPE
    )

    pipe.stdin.write(ppm_data)

    pipe.stdin.close()
    pipe.wait()
    pipe.terminate()

    print(f'INFO: Image created at {repr(file_path)}.')
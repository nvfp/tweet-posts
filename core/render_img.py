import os, subprocess as sp
from .shared import FFMPEG, RENDERED_IMG_PTH, RENDERED_IMG_PTH2, IMG_RES

def render_with_stats(
    ppm_data,

    edit_contrast,
    edit_brightness,
    edit_saturation,
    edit_gamma,
    edit_gamma_r,
    edit_gamma_g,
    edit_gamma_b,
    edit_vignette,
    edit_temp,

    data_pack,
):
    def render_fractal_img():
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
            RENDERED_IMG_PTH2
        ]
        # if os.path.exists(RENDERED_IMG_PTH): raise AssertionError
        pipe = sp.Popen(cmd, stdin=sp.PIPE)
        pipe.stdin.write(ppm_data)
        pipe.stdin.close()
        pipe.wait()
        pipe.terminate()

        # file_size = os.path.getsize(file_path)
        # return file_size  # metadata purposes
    render_fractal_img()
    
    PAD = 33
    filter_complex = f"color=s={IMG_RES[0]+2*PAD}x{IMG_RES[1]+1100}:c=0x3b3b3b[bg];[bg][0]overlay=x={PAD}:y={PAD}"
    
    def get_text_filters():
        out = []
        Y_ANCHOR = 230
        Y_GAP = 51
        out.append(f"drawtext=text='xmin={data_pack['xmin']}':x=130:y={IMG_RES[1]+Y_ANCHOR}:fontcolor=0xffffff:fontsize=71")
        out.append(f"drawtext=text='xmax={data_pack['xmax']}':x=130:y='{IMG_RES[1]+Y_ANCHOR+Y_GAP}+th':fontcolor=0xffffff:fontsize=71")
        out.append(f"drawtext=text='ymin={data_pack['ymin']}':x=130:y={IMG_RES[1]+Y_ANCHOR+Y_GAP*2}+th*2:fontcolor=0xffffff:fontsize=71")
        out.append(f"drawtext=text='ymax={data_pack['ymax']}':x=130:y='{IMG_RES[1]+Y_ANCHOR+Y_GAP*3}+th*3':fontcolor=0xffffff:fontsize=71")
        return out
    filter_complex = f"{filter_complex},{','.join(get_text_filters())}"
    
    cmd = [
        FFMPEG,
        '-i', RENDERED_IMG_PTH2,
        '-filter_complex', filter_complex,
        '-frames:v', '1',
        '-q:v', '0',
        RENDERED_IMG_PTH
    ]
    sp.call(cmd)


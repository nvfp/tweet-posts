import os, subprocess as sp, random
from .shared import FFMPEG, RENDERED_IMG_PTH, RENDERED_IMG_PTH2, IMG_RES
from .utils import hsl_to_hex, get_ffmpeg_drawtext_filter

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
    
    XPAD = 51
    BORDER_THICK = 13
    Y_OFF = 311
    filter_complex = (
        # f"color=s={IMG_RES[0]+2*PAD}x{IMG_RES[1]+1700}:c={hsl_to_hex(random.randint(0,359),0.71,0.13)}[bg];"
        # f"color=s={IMG_RES[0]+2*BORDER_THICK}x{IMG_RES[1]+2*BORDER_THICK}:c={hsl_to_hex(random.randint(0,359),0.71,0.87)}[border];"
        # f"[bg][border]overlay=x={PAD}:y={PAD+297}"
        # f"[bg][0]overlay=x={PAD+BORDER_THICK}:y={PAD+297+BORDER_THICK}"
        f"color=s={IMG_RES[0]+2*XPAD+2*BORDER_THICK}x{IMG_RES[1]+1700}:c={hsl_to_hex(random.randint(0,359),0.71,0.09)}[bg];"
        f"color=s={IMG_RES[0]+2*BORDER_THICK}x{IMG_RES[1]+2*BORDER_THICK}:c={hsl_to_hex(random.randint(0,359),0.71,0.87)}[border];"
        f"[bg][border]overlay=x={XPAD}:y={Y_OFF}[bg];"
        f"[bg][0]overlay=x={XPAD+BORDER_THICK}:y={Y_OFF+BORDER_THICK}"
    )
    
    def get_text_filters():
        out = []
        Y_ANCHOR = 230
        Y_GAP = 51
        # out.append(f"drawtext=text='x-min={data_pack['xmin']}':x=130:y={IMG_RES[1]+Y_ANCHOR}:fontcolor=0xffffff:fontsize=71")
        # out.append(f"drawtext=text='x-max={data_pack['xmax']}':x=130:y='{IMG_RES[1]+Y_ANCHOR+Y_GAP}+th':fontcolor=0xffffff:fontsize=71")
        # out.append(f"drawtext=text='y-min={data_pack['ymin']}':x=130:y={IMG_RES[1]+Y_ANCHOR+Y_GAP*2}+th*2:fontcolor=0xffffff:fontsize=71")
        # out.append(f"drawtext=text='y-max={data_pack['ymax']}':x=130:y='{IMG_RES[1]+Y_ANCHOR+Y_GAP*3}+th*3':fontcolor=0xffffff:fontsize=71")

        font = '/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf'
        font2 = '/usr/share/fonts/truetype/lato/Lato-Black.ttf'
        font3 = '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf'

        out.append(get_ffmpeg_drawtext_filter(data_pack['fractal_name'], '(w-tw)*0.5', 51, hsl_to_hex(random.randint(0,359),0.5,0.91), 201, font2))

        y = IMG_RES[1] + 393
        out.append(get_ffmpeg_drawtext_filter(f"Find me at", '(w-tw)*0.5', y, hsl_to_hex(random.randint(0,359),0.71,0.77), 151, font2))
        
        y += 211
        color = '0xc7c7c7'
        size = 93
        xpad = 131
        out.append(get_ffmpeg_drawtext_filter(f"X-min\: {data_pack['xmin']}", xpad, f"{y+51*0}+th*0", color, size, font3))
        out.append(get_ffmpeg_drawtext_filter(f"X-max\: {data_pack['xmax']}", xpad, f"{y+51*1}+th*1", color, size, font3))
        out.append(get_ffmpeg_drawtext_filter(f"Y-min\: {data_pack['ymin']}", xpad, f"{y+51*2+17}+th*2", color, size, font3))
        out.append(get_ffmpeg_drawtext_filter(f"Y-max\: {data_pack['ymax']}", xpad, f"{y+51*3+17}+th*3", color, size, font3))
        
        size = 57
        y += 613
        color = '0xb3b3b3'
        out.append(get_ffmpeg_drawtext_filter(f"Number of iterations\: {data_pack['nIter']:,}", xpad, f"{y}+th*0", color, size, font3))
        out.append(get_ffmpeg_drawtext_filter(f"Size\: {round(os.path.getsize(RENDERED_IMG_PTH2)/1000_000,2)} mB", xpad, f"{y+51}+th*1", color, size, font3))
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


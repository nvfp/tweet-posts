import random

def get_ffmpeg_filter_vals():
    edit_contrast   = round( random.uniform(0.7, 1.8)  , 2 )
    edit_brightness = round( random.uniform(-0.1, 0.23), 2 )
    edit_saturation = round( random.uniform(0.25, 1.75), 2 )
    edit_gamma      = round( random.uniform(0.9, 1.1)  , 2 )
    edit_gamma_r    = round( random.uniform(0.9, 1.1)  , 2 )
    edit_gamma_g    = round( random.uniform(0.9, 1.1)  , 2 )
    edit_gamma_b    = round( random.uniform(0.9, 1.1)  , 2 )
    edit_vignette   = random.randint(-48, 33)
    edit_temp       = random.randint(2000, 8000)
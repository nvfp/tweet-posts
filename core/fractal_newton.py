import random, time, numpy as np, numba as nb
from .shared import IMG_RES
from .post_online import post_online
from .write_md import write_metadata_file
from .get_ppm import get_ppm
from .render_img import render_with_stats

FRACTAL_NAME = 'Newton'  # will be used in post's description

NEWTON_POWER = random.randint(3, 11)
NEWTON_CONST = random.randint(-10, 10)
@nb.jit(nb.int32(nb.complex128, nb.int32))
def _get_esc_iter(c_frag, n_iter_frag):
    z = c_frag
    for n in range(n_iter_frag):
        f_value = np.power(z, NEWTON_POWER) + NEWTON_CONST
        f_prime_value = NEWTON_POWER*np.power(z, NEWTON_POWER-1)
        if abs(f_value) < 1e-6:
            return n
        z = z - f_value / f_prime_value
    return 0
@nb.guvectorize([(nb.complex128[:], nb.int32[:], nb.int32[:])], '(n),()->(n)', target='parallel')
def _get_iter_mtrx(c_mtrx, n_iter, iter_mtrx):
    n_iter_frag = n_iter[0]  # fragment
    for i in range(c_mtrx.shape[0]):
        iter_mtrx[i] = _get_esc_iter(c_mtrx[i], n_iter_frag)
def compute_array(w, h, xmin, xmax, ymin, ymax, antialiasing_is_on, antialiasing_supsample, n_iter):
    if antialiasing_is_on:
        w = w * antialiasing_supsample
        h = h * antialiasing_supsample
    x_mtrx = np.linspace(xmin, xmax, w, dtype=np.float64)
    y_mtrx = np.linspace(ymax, ymin, h, dtype=np.float64)
    c_mtrx = x_mtrx + y_mtrx[:,None] * 1j
    raw = _get_iter_mtrx(c_mtrx, n_iter)
    return raw
def get_raw_grayscale_image(
    w, h,
    antialiasing_is_on,
    antialiasing_supsample,
    n_iter,
    xmin, xmax,
    ymin, ymax
):
    raw = compute_array(w, h, xmin, xmax, ymin, ymax, antialiasing_is_on, antialiasing_supsample, n_iter)
    if antialiasing_is_on: raw = raw.reshape(h, antialiasing_supsample, w, antialiasing_supsample).mean(3).mean(1)
    return raw

def get_random_range():

    ## The region where the fractal is visible
    x_bound_min = -3
    x_bound_max = 3
    y_bound_min = -2
    y_bound_max = 2

    total_width = x_bound_max - x_bound_min
    # total_height = y_bound_max - y_bound_min

    ## The captured one
    frame_width = total_width/random.randint(1, 100)
    frame_height = frame_width*(IMG_RES[1] / IMG_RES[0])  # based on aspect ratio

    xmin = random.uniform(x_bound_min, x_bound_max-frame_width)
    xmax = xmin + frame_width

    ymin = random.uniform(y_bound_min, y_bound_max-frame_height)
    ymax = ymin + frame_height

    return xmin, xmax, ymin, ymax

def find_fractal():

    # n_iter = random.randint(128, 512)

    data_pack = {}
    
    k = 0
    t = time.time()
    std = -1  # standard deviation
    nIter, xmin, xmax, ymin, ymax = None, None, None, None, None
    
    # while (std < 20) or (time.time()-t < 3600):  # this based on std , but let's just use based on hours
    while std < 3:
        k += 1
        
        _nIter = random.randint(250, 1000)
        _xmin, _xmax, _ymin, _ymax = get_random_range()
        
        raw = get_raw_grayscale_image(round(IMG_RES[0]/2), round(IMG_RES[1]/2), False, 2, _nIter, _xmin, _xmax, _ymin, _ymax)  # during search, dont use antialiasing, and use lower resolution for faster search.
        _std = np.std(raw)
        
        if _std > std:
            std = _std    
            nIter = _nIter
            xmin, xmax, ymin, ymax = _xmin, _xmax, _ymin, _ymax

    # dur = time.time() - dur_t0
    the_raw = get_raw_grayscale_image(IMG_RES[0], IMG_RES[1], True, 3, nIter, xmin, xmax, ymin, ymax)

    data_pack['xmin'] = xmin
    data_pack['xmax'] = xmax
    data_pack['ymin'] = ymin
    data_pack['ymax'] = ymax
    data_pack['nIter'] = nIter

    return the_raw, data_pack

def run_burning_ship():

    data_pack = {}
    
    ct = random.randint(1, 255)  # PPM color threshold
    hue_offset = random.randint(0, 359)
    saturation = round( random.uniform(-1, 1), 2 )

    the_raw, find_fractal_data_pack = find_fractal()
    for k,v in find_fractal_data_pack.items():
        if k in data_pack: raise AssertionError(f"Duplicated: {k}")
        data_pack[k] = v

    ppm_data = get_ppm(the_raw, IMG_RES[0], IMG_RES[1], ct, hue_offset, saturation)

    ## Random FFmpeg filters
    edit_contrast   = round( random.uniform(0.7, 1.8)  , 2 )
    edit_brightness = round( random.uniform(-0.1, 0.23), 2 )
    edit_saturation = round( random.uniform(0.25, 1.75), 2 )
    edit_gamma      = round( random.uniform(0.9, 1.1)  , 2 )
    edit_gamma_r    = round( random.uniform(0.9, 1.1)  , 2 )
    edit_gamma_g    = round( random.uniform(0.9, 1.1)  , 2 )
    edit_gamma_b    = round( random.uniform(0.9, 1.1)  , 2 )
    edit_vignette   = random.randint(-51, -13)
    edit_temp       = random.randint(2000, 8000)

    # Export
    # file_size = save_img(
    #     IMAGE_PTH,
    #     ppm_data,

    #     edit_contrast,
    #     edit_brightness,
    #     edit_saturation,
    #     edit_gamma,
    #     edit_gamma_r,
    #     edit_gamma_g,
    #     edit_gamma_b,
    #     edit_vignette,
    #     edit_temp
    # )

    render_with_stats(
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
    )

    ## Posting
    out = post_online(FRACTAL_NAME)


    # write_metadata_file(FRACTAL_NAME,)
    # md_pack = {
        
    # }

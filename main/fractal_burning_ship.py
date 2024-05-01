import random, time, numpy as np, numba as nb
from .get_ppm import get_ppm
from .save_image import saveImg
from .upload import upload

@nb.jit(nb.int32(nb.complex128, nb.int32))
def _get_esc_iter(c_frag, n_iter_frag):
    nreal = 0
    real = 0
    imag = 0
    for n in range(n_iter_frag):
        nreal = abs(real)*abs(real) - abs(imag)*abs(imag) + c_frag.real
        imag = 2*abs(real)*abs(imag) + c_frag.imag
        real = nreal
        if real*real + imag*imag > 255*255:
            return n + 4 - np.log2(np.log2(real*real + imag*imag))
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

def getRandomRange(resW, resH):

    ## The region where the fractal is visible
    x_bound_min = -2.5
    x_bound_max = 2
    y_bound_min = -2.1
    y_bound_max = 0.9

    total_width = x_bound_max - x_bound_min
    # total_height = y_bound_max - y_bound_min

    ## The captured one
    frame_width = total_width/random.randint(1, 10)
    frame_height = frame_width*(resH/resW)  # based on aspect ratio

    xmin = random.uniform(x_bound_min, x_bound_max-frame_width)
    xmax = xmin + frame_width

    ymin = random.uniform(y_bound_min, y_bound_max-frame_height)
    ymax = ymin + frame_height

    return xmin, xmax, ymin, ymax

def findFractal(resW,resH):

    std = -1  # standard deviation
    nIter, xmin, xmax, ymin, ymax = None, None, None, None, None
    
    while std < 7:  # just based on std, not time because too high std might give images that are too noisy
        
        _nIter = random.randint(250, 1000)
        _xmin,_xmax, _ymin,_ymax = getRandomRange(resW,resH)
        
        raw = get_raw_grayscale_image(round(resW/2),round(resH/2), False, 2, _nIter, _xmin,_xmax, _ymin,_ymax)  # during search, dont use antialiasing, and use lower resolution for faster search.
        _std = np.std(raw)
        
        if _std > std:
            std = _std    
            nIter = _nIter
            xmin, xmax, ymin, ymax = _xmin, _xmax, _ymin, _ymax

    the_raw = get_raw_grayscale_image(resW,resH, True, 3, nIter, xmin, xmax, ymin, ymax)
    return the_raw

def runBurningShip():

    IMG_RES = [2000, 2000]
    OUTPUT_PTH = './_the_rendered_image.jpg'

    the_raw = findFractal(IMG_RES[0], IMG_RES[1])
    ppmData = get_ppm(
        raw=the_raw,
        w=IMG_RES[0],h=IMG_RES[1], 
        ct=random.randint(1, 255),  # PPM color threshold
        hue_offset=random.randint(0, 359),
        saturation=round( random.uniform(-1, 1), 2 ),
    )
    saveImg(
        edit_contrast=round( random.uniform(0.7, 1.8)  , 2 ),
        edit_brightness=round( random.uniform(-0.1, 0.23), 2 ),
        edit_saturation=round( random.uniform(0.25, 1.75), 2 ),
        edit_gamma=round( random.uniform(0.9, 1.1)  , 2 ),
        edit_gamma_r=round( random.uniform(0.9, 1.1)  , 2 ),
        edit_gamma_g=round( random.uniform(0.9, 1.1)  , 2 ),
        edit_gamma_b=round( random.uniform(0.9, 1.1)  , 2 ),
        edit_vignette=random.randint(-51, -13),
        edit_temp=random.randint(2000, 8000),
        
        ppm_data=ppmData,
        outputPth=OUTPUT_PTH,
    )
    upload(OUTPUT_PTH)

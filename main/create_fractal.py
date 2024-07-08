"""todo: centerize the final fractal, do auto compute for fractal boundary"""
import subprocess as sp,os,random,numpy as np
from .get_ppm import get_ppm
from .upload import upload

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

    ppmData,
    outputPth,
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
        outputPth
    ], stdin=sp.PIPE)
    pipe.stdin.write(ppmData)
    pipe.stdin.close()
    pipe.wait()
    pipe.terminate()

    print(f"Image saved ({round(os.path.getsize(outputPth)/1000,1)} kB)")



def compute_array(w, h, xmin, xmax, ymin, ymax, antialiasing_is_on, antialiasing_supsample, n_iter, _get_iter_mtrx):
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
    ymin, ymax,

    _get_iter_mtrx
):
    raw = compute_array(w, h, xmin, xmax, ymin, ymax, antialiasing_is_on, antialiasing_supsample, n_iter, _get_iter_mtrx)
    if antialiasing_is_on: raw = raw.reshape(h, antialiasing_supsample, w, antialiasing_supsample).mean(3).mean(1)
    return raw  # is 2d np array
def getRandomRange(resW,resH, xRegMin,xRegMax, yRegMin,yRegMax, scale_factor):# [xRegMin/max: is the region where the fractal is visible]
    
    total_width  = xRegMax-xRegMin
    total_height = yRegMax-yRegMin
    
    frame_width = total_width/random.randint(1, scale_factor)#the captured one
    frame_height = frame_width*(resH/resW)  # based on aspect ratio

    xmin = random.uniform(xRegMin, xRegMax-frame_width)
    xmax = xmin + frame_width

    ymin = random.uniform(yRegMin, yRegMax-frame_height)
    ymax = ymin + frame_height

    return xmin,xmax, ymin,ymax
def findFractal(resW,resH, std_min, nIter_min,nIter_max, _get_iter_mtrx, xRegMin,xRegMax, yRegMin,yRegMax, scale_factor):

    std = -1  # standard deviation
    nIter, xmin,xmax, ymin,ymax = 0,0,0,0,0
    while std < std_min:
        nIter = random.randint(nIter_min,nIter_max)
        xmin,xmax, ymin,ymax = getRandomRange(resW,resH, xRegMin,xRegMax, yRegMin,yRegMax, scale_factor)
        
        sample = get_raw_grayscale_image(round(resW/2),round(resH/2), False, 2, nIter, xmin,xmax, ymin,ymax, _get_iter_mtrx)  # during search, dont use antialiasing, and use lower resolution for faster search.
        padRatio=0.13  # doing these, so the image concentrated in the middle
        sampleH,sampleW=sample.shape
        tlx=round(sampleW*padRatio)
        drx=sampleW-tlx
        tly=round(sampleH*padRatio)
        dry=sampleH-tly
        std = np.std(sample[tly:dry+1, tlx:drx+1])
        
    return get_raw_grayscale_image(resW,resH, True, 5, nIter, xmin, xmax, ymin, ymax, _get_iter_mtrx)  # Return the full quality

def createFractal(std_min, nIter_min,nIter_max, _get_iter_mtrx, xRegMin,xRegMax, yRegMin,yRegMax, scale_factor):

    IMG_RES = [1500,1500]
    OUTPUT_PTH = './out.jpg'

    the_raw = findFractal(IMG_RES[0], IMG_RES[1], std_min, nIter_min,nIter_max, _get_iter_mtrx, xRegMin,xRegMax, yRegMin,yRegMax, scale_factor)
    ppmData = get_ppm(
        raw=the_raw,
        w=IMG_RES[0],h=IMG_RES[1], 
        ct=255,  # PPM color threshold
        hue_offset=random.randint(0,359),
        saturation=random.uniform(0.9,1.1),
    )
    saveImg(
        edit_contrast   = random.uniform(1.3,1.7),
        edit_brightness = random.uniform(-0.03, 0.03),
        edit_saturation = random.uniform(0.75, 1.25),
        edit_gamma      = random.uniform(0.9, 1.1),
        edit_gamma_r    = random.uniform(0.9, 1.1),
        edit_gamma_g    = random.uniform(0.9, 1.1),
        edit_gamma_b    = random.uniform(0.9, 1.1),
        edit_vignette   = random.randint(-59,-39),
        edit_temp       = random.randint(1900,3500),
        
        ppmData=ppmData,
        outputPth=OUTPUT_PTH,
    )
    upload(OUTPUT_PTH)

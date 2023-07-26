import numba as nb
import numpy as np

from mykit.kit.utils import printer


@nb.njit
def _hsv_to_rgb(h, s, v):

    h_frac = h / 60
    h_modu = np.floor(h_frac) % 6

    f = h_frac - h_modu
    p = v * (1 - s)
    q = v * (1 - f*s)
    t = v * (1- (1 - f)*s)

    if h_modu == 0: return int(v * 255), int(t * 255), int(p * 255)
    if h_modu == 1: return int(q * 255), int(v * 255), int(p * 255)
    if h_modu == 2: return int(p * 255), int(v * 255), int(t * 255)
    if h_modu == 3: return int(p * 255), int(q * 255), int(v * 255)
    if h_modu == 4: return int(t * 255), int(p * 255), int(v * 255)
    if h_modu == 5: return int(v * 255), int(p * 255), int(q * 255)


@nb.njit
def _convert(arr, hue_offset, saturation):

    img_arr = np.zeros(3 * arr.size)

    for idx, (row, col) in enumerate(np.ndindex(arr.shape)):
        clr = arr[row][col] % 256
        rat = clr / 255

        h = (rat*360 + hue_offset) % 360
        s = saturation
        v = np.sqrt(rat)  # The darker pixels will remain dark

        r, g, b = _hsv_to_rgb(h, s, v)

        img_arr[idx*3    ] = r
        img_arr[idx*3 + 1] = g
        img_arr[idx*3 + 2] = b

    return img_arr


def get_ppm(raw, w, h, ct, hue_offset, saturation):
    printer('DEBUG: Generating the ppm data.')
    raw = _convert(raw, hue_offset, saturation)
    ppm = f'P6 {w} {h} {ct} '.encode()
    ppm += raw.astype(np.uint8).tobytes()
    return ppm
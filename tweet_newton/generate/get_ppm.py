import numba as nb
import numpy as np

from mykit.kit.utils import printer


power = None
const = None
def change_newton(set_power, set_const):
    global power, const
    power = set_power
    const = set_const


@nb.jit(nb.int32(nb.complex128, nb.int32))
def _get_esc_iter(c_frag, n_iter_frag):
    z = c_frag
    for n in range(n_iter_frag):
        f_value = np.power(z, power) + const
        f_prime_value = power*np.power(z, power-1)
        if abs(f_value) < 1e-6:
            return n
        z = z - f_value / f_prime_value
    return 0

@nb.guvectorize([(nb.complex128[:], nb.int32[:], nb.int32[:])], '(n),()->(n)', target='parallel')
def _get_iter_mtrx(c_mtrx, n_iter, iter_mtrx):
    n_iter_frag = n_iter[0]  # fragment
    for i in range(c_mtrx.shape[0]):
        iter_mtrx[i] = _get_esc_iter(c_mtrx[i], n_iter_frag)

def compute_array_numba(w, h, xmin, xmax, ymin, ymax, antialiasing_is_on, antialiasing_supsample, n_iter):

    if antialiasing_is_on:
        w = w * antialiasing_supsample
        h = h * antialiasing_supsample

    x_mtrx = np.linspace(xmin, xmax, w, dtype=np.float64)
    y_mtrx = np.linspace(ymax, ymin, h, dtype=np.float64)

    c_mtrx = x_mtrx + y_mtrx[:,None] * 1j
    
    raw = _get_iter_mtrx(c_mtrx, n_iter)
    return raw


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


def get_raw_grayscale_image(
    w, h,
    antialiasing_is_on,
    antialiasing_supsample,
    n_iter,
    xmin, xmax,
    ymin, ymax
):
    raw = compute_array_numba(w, h, xmin, xmax, ymin, ymax, antialiasing_is_on, antialiasing_supsample, n_iter)
    if antialiasing_is_on:
        raw = raw.reshape(h, antialiasing_supsample, w, antialiasing_supsample).mean(3).mean(1)
    return raw


def get_ppm(
    raw,
    w, h, ct,
    hue_offset, saturation
):
    printer('DEBUG: Generating the ppm data.')
    raw = _convert(raw, hue_offset, saturation)
    ppm = f'P6 {w} {h} {ct} '.encode()
    ppm += raw.astype(np.uint8).tobytes()
    return ppm
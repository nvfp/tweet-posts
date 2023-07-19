import numba as nb
import numpy as np


def compute_array_numpy(w, h, xmin, xmax, ymin, ymax, antialiasing_is_on, antialiasing_supsample, n_iter, degree, r_conv):

    if antialiasing_is_on:
        w = w * antialiasing_supsample
        h = h * antialiasing_supsample

    x_mtrx = np.linspace(xmin, xmax, w).reshape((1, w))
    y_mtrx = np.linspace(ymax, ymin, h).reshape((h, 1))

    c_mtrx = x_mtrx + 1j*y_mtrx

    z_mtrx = np.zeros(c_mtrx.shape, dtype=np.complex128)
    has_not_diverged = np.full(c_mtrx.shape, True, dtype=bool)
    iter_mtrx = np.zeros(z_mtrx.shape, dtype=int)

    for iter in range(1, n_iter + 1):

        ## just iterate pixels that have not diverged
        z_mtrx[has_not_diverged] = (z_mtrx[has_not_diverged] ** degree) + c_mtrx[has_not_diverged]
        ## faster it diverges -> smaller its luminance.
        ## never diverged (the Mandelbrot set) -> 0 luminance
        diverged = np.greater(
            np.abs(z_mtrx),
            r_conv,
            out=np.full(c_mtrx.shape, False),
            where=has_not_diverged
        )
        iter_mtrx[diverged] = iter
        has_not_diverged[np.abs(z_mtrx) > r_conv] = False
    
    raw = iter_mtrx
    return raw


@nb.jit(nb.int32(nb.complex128, nb.int32))
def _get_esc_iter(c_frag, n_iter_frag):
    nreal = 0
    real = 0
    imag = 0

    for n in range(n_iter_frag):
        nreal = real*real - imag*imag + c_frag.real
        imag = 2*real*imag + c_frag.imag
        real = nreal
        if real*real + imag*imag > 255*255:
            return n + 4 - np.log2(np.log2(real*real + imag*imag))
    return 0

@nb.guvectorize([(nb.complex128[:], nb.int32[:], nb.int32[:])], '(n),()->(n)', target='parallel')
def _get_iter_mtrx(c_mtrx, n_iter, iter_mtrx):
    n_iter_frag = n_iter[0]  # fragment
    for i in range(c_mtrx.shape[0]):
        iter_mtrx[i] = _get_esc_iter(c_mtrx[i], n_iter_frag)

def compute_array_numba(w, h, xmin, xmax, ymin, ymax, antialiasing_is_on, antialiasing_supsample, n_iter, degree, r_conv):

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

        # h = (rat*360 + hue_offset) % 360
        # s = rat
        # v = 0.75 if clr not in (0, 255) else 0

        h = (rat*360 + hue_offset) % 360
        s = saturation
        v = np.sqrt(rat)  # darker pixel will remain dark

        r, g, b = _hsv_to_rgb(h, s, v)

        img_arr[idx*3    ] = r
        img_arr[idx*3 + 1] = g
        img_arr[idx*3 + 2] = b
    return img_arr


def get_raw_grayscale_image(
    use_fast_renderer,
    w, h,
    antialiasing_is_on,
    antialiasing_supsample,
    n_iter,
    degree,
    r_conv,
    xmin, xmax,
    ymin, ymax
):

    if use_fast_renderer:
        raw = compute_array_numba(w, h, xmin, xmax, ymin, ymax, antialiasing_is_on, antialiasing_supsample, n_iter, degree, r_conv)
    else:
        raw = compute_array_numpy(w, h, xmin, xmax, ymin, ymax, antialiasing_is_on, antialiasing_supsample, n_iter, degree, r_conv)

    if antialiasing_is_on:
        raw = raw.reshape(h, antialiasing_supsample, w, antialiasing_supsample).mean(3).mean(1)
    
    return raw


def get_ppm(
    raw,
    is_grayscale,
    w, h, ct,
    hue_offset, saturation
):

    if not is_grayscale:
        raw = _convert(raw, hue_offset, saturation)

    if is_grayscale:
        ppm = f'P5 {w} {h} {ct} '.encode()
    else:
        ppm = f'P6 {w} {h} {ct} '.encode()
    ppm += raw.astype(np.uint8).tobytes()

    return ppm
import numba as nb
import numpy as np
import random


newton_power = random.randint(3, 7)
newton_const = random.randint(-10, 10)

@nb.jit(nb.int32(nb.complex128, nb.int32))
def _get_esc_iter(c_frag, n_iter_frag):
    z = c_frag
    for n in range(n_iter_frag):
        f_value = np.power(z, newton_power) + newton_const
        f_prime_value = newton_power*np.power(z, newton_power-1)
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
    if antialiasing_is_on:
        raw = raw.reshape(h, antialiasing_supsample, w, antialiasing_supsample).mean(3).mean(1)
    return raw
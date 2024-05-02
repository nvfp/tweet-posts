import numba as nb,numpy as np
from .create_fractal import createFractal

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


def runMandelbrot():
    createFractal(17, 128,4096, _get_iter_mtrx,-2.75,1.25, -1.124,1.13, 10000)

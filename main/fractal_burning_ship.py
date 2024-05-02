import numba as nb,numpy as np
from .create_fractal import createFractal

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



def runBurningShip():
    createFractal(7, 128,2048, _get_iter_mtrx,-2.5,2, -2.1,0.9, 17)

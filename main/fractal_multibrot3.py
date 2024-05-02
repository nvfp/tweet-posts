import numba as nb
from .create_fractal import createFractal

@nb.jit(nb.int32(nb.complex128, nb.int32))
def _get_esc_iter(c_frag, n_iter_frag):
    z = 0j
    for n in range(n_iter_frag):
        z = z*z*z + c_frag
        if abs(z) > 2:
            return n
    return 0
@nb.guvectorize([(nb.complex128[:], nb.int32[:], nb.int32[:])], '(n),()->(n)', target='parallel')
def _get_iter_mtrx(c_mtrx, n_iter, iter_mtrx):
    n_iter_frag = n_iter[0]  # fragment
    for i in range(c_mtrx.shape[0]):
        iter_mtrx[i] = _get_esc_iter(c_mtrx[i], n_iter_frag)

def runMultibrot3():
    createFractal(9, 128,2048, _get_iter_mtrx,-2,2, -1.5,1.5, 1000)
    
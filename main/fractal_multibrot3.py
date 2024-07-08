import numba as nb,random
from .create_fractal import createFractal

@nb.jit(nb.int32(nb.complex128, nb.int32))
def getEscIter_deg3(c_frag, n_iter_frag):
    z = 0j
    for n in range(n_iter_frag):
        z = z*z*z + c_frag
        if abs(z) > 2:
            return n
    return 0
@nb.guvectorize([(nb.complex128[:], nb.int32[:], nb.int32[:])], '(n),()->(n)', target='parallel')
def getIterMtrx_deg3(c_mtrx, n_iter, iter_mtrx):
    n_iter_frag = n_iter[0]  # fragment
    for i in range(c_mtrx.shape[0]):
        iter_mtrx[i] = getEscIter_deg3(c_mtrx[i], n_iter_frag)

def runMultibrot3():
    createFractal(15, 1000,3000, getIterMtrx_deg3,-2,2, -1.5,1.5, 1000)

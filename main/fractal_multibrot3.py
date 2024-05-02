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

@nb.jit(nb.int32(nb.complex128, nb.int32))
def getEscIter_deg5(c_frag, n_iter_frag):
    z = 0j
    for n in range(n_iter_frag):
        z = z*z*z*z*z + c_frag
        if abs(z) > 2:
            return n
    return 0
@nb.guvectorize([(nb.complex128[:], nb.int32[:], nb.int32[:])], '(n),()->(n)', target='parallel')
def getIterMtrx_deg5(c_mtrx, n_iter, iter_mtrx):
    n_iter_frag = n_iter[0]  # fragment
    for i in range(c_mtrx.shape[0]):
        iter_mtrx[i] = getEscIter_deg5(c_mtrx[i], n_iter_frag)

@nb.jit(nb.int32(nb.complex128, nb.int32))
def getEscIter_deg7(c_frag, n_iter_frag):
    z = 0j
    for n in range(n_iter_frag):
        z = z*z*z*z*z*z*z + c_frag
        if abs(z) > 2:
            return n
    return 0
@nb.guvectorize([(nb.complex128[:], nb.int32[:], nb.int32[:])], '(n),()->(n)', target='parallel')
def getIterMtrx_deg7(c_mtrx, n_iter, iter_mtrx):
    n_iter_frag = n_iter[0]  # fragment
    for i in range(c_mtrx.shape[0]):
        iter_mtrx[i] = getEscIter_deg7(c_mtrx[i], n_iter_frag)

def runMultibrot3():
    k=random.choice([3,5,7])
    if k==3:
        createFractal(9, 128,2048, getIterMtrx_deg3,-2,2, -1.5,1.5, 1000)
    elif k==5:
        createFractal(7, 128,1024, getIterMtrx_deg5,-2,2, -1.5,1.5, 100)
    elif k==7:
        createFractal(5, 64,512, getIterMtrx_deg7,-2,2, -1.5,1.5, 10)
    else:
        raise AssertionError

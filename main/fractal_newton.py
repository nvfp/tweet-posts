import numba as nb,random,numpy as np
from .create_fractal import createFractal


NEWTON_POWER = random.randint(3, 11)# i think should be outside
NEWTON_CONST = random.randint(-10, 10)
@nb.jit(nb.int32(nb.complex128, nb.int32))
def _get_esc_iter(c_frag, n_iter_frag):
    # NEWTON_POWER = random.randint(3, 11)
    # NEWTON_CONST = random.randint(-10, 10)
    z = c_frag
    for n in range(n_iter_frag):
        f_value = np.power(z, NEWTON_POWER) + NEWTON_CONST
        f_prime_value = NEWTON_POWER*np.power(z, NEWTON_POWER-1)
        if abs(f_value) < 1e-6:
            return n
        z = z - f_value / f_prime_value
    return 0
@nb.guvectorize([(nb.complex128[:], nb.int32[:], nb.int32[:])], '(n),()->(n)', target='parallel')
def _get_iter_mtrx(c_mtrx, n_iter, iter_mtrx):
    n_iter_frag = n_iter[0]  # fragment
    for i in range(c_mtrx.shape[0]):
        iter_mtrx[i] = _get_esc_iter(c_mtrx[i], n_iter_frag)



def runNewton():
    createFractal(3, 128,1024, _get_iter_mtrx,-3,3, -2,2, 100)

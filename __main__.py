import sys, os
sys.path.append(os.path.dirname(__file__))  # make the folders importable
from core.fractal_burning_ship import run_burning_ship
from core.fractal_mandelbrot import run_mandelbrot
# from core.fractal_multibrot3 import run_multibrot3
from core.fractal_newton import run_newton

def get_fractal_name():
    args = sys.argv
    if len(args) != 2: raise AssertionError(f"Need 1 positional arg, the fractal name.")
    return args[1]

def main():
    name = get_fractal_name()
    if name == 'BurningShip': run_burning_ship()
    elif name == 'MandelbrotSet': run_mandelbrot()
    # elif name == 'Multibrot3': run_multibrot3()
    elif name == 'Newton': run_newton()
    else: raise AssertionError(f"Invalid: {name}")

if __name__ == '__main__':
    main()

import random
from main.fractal_mandelbrot import runMandelbrot
from main.fractal_multibrot3 import runMultibrot3
from main.fractal_newton import runNewton
from main.fractal_burning_ship import runBurningShip

if __name__ == '__main__':
    random.choice([runMandelbrot, runMultibrot3, runNewton, runBurningShip])()

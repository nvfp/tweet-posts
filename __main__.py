import random
from main.fractal_mandelbrot import runMandelbrot
from main.fractal_multibrot3 import runMultibrot3
from main.fractal_newton import runNewton
from main.fractal_burning_ship import runBurningShip

if __name__ == '__main__':
    # k=random.randint(0,3)
    k=random.choice([run_burning_ship,run_mandelbrot,run_multibrot3,run_newton])
    k()

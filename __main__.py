import random
from main.fractal_multibrot3 import runMultibrot3
from main.fractal_newton import runNewton

if __name__ == '__main__':
    random.choice([runMultibrot3, runNewton])()

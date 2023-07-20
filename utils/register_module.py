import os
import sys

from mykit.kit.utils import printer


if __name__ == '__main__':

    PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    printer(f'DEBUG: Appending {repr(PROJECT_ROOT_DIR)} to `sys.path`.')
    sys.path.append(PROJECT_ROOT_DIR)
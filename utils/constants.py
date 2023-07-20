import os

from mykit.kit.utils import printer


PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
printer(f'DEBUG: PROJECT_ROOT_DIR: {repr(PROJECT_ROOT_DIR)}.')
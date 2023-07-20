import os

from mykit.kit.utils import printer


REPO_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
printer(f'DEBUG: REPO_ROOT_DIR: {repr(REPO_ROOT_DIR)}.')
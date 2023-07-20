import os

from mykit.kit.utils import printer

from utils.constants import PROJECT_ROOT_DIR


ARCHIVE_DIR = os.path.join(PROJECT_ROOT_DIR, 'tweet_mandelbrot', 'archive')
DRAFT_DIR   = os.path.join(PROJECT_ROOT_DIR, 'tweet_mandelbrot', 'draft')
printer(f'DEBUG: ARCHIVE_DIR: {repr(ARCHIVE_DIR)}.')
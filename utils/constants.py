import os

from mykit.kit.utils import printer


TOP_LEVEL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
printer(f'DEBUG: TOP_LEVEL_DIR: {repr(TOP_LEVEL_DIR)}.')

ARCHIVE_TEMP_DIR = os.path.join(TOP_LEVEL_DIR, '__archive_temp_dir__')
printer(f'DEBUG: ARCHIVE_TEMP_DIR: {repr(ARCHIVE_TEMP_DIR)}.')


REPO_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
printer(f'DEBUG: REPO_ROOT_DIR: {repr(REPO_ROOT_DIR)}.')

# This one should mirror the one in .github/workflows/tweet-mandelbrot-fractals-hourly.yml
FFMPEG = os.path.join(REPO_ROOT_DIR, 'THE_VENV_CACHE', 'FFMPEG_BIN', 'ffmpeg')
printer(f'DEBUG: FFMPEG: {repr(FFMPEG)}.')
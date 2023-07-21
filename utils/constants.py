import os

from mykit.kit.utils import printer


REPO_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
printer(f'DEBUG: REPO_ROOT_DIR: {repr(REPO_ROOT_DIR)}.')

# This one should mirror the one in .github/workflows/tweet-mandelbrot-fractals-hourly.yml
FFMPEG = os.path.join(REPO_ROOT_DIR, 'THE_VENV_CACHE', 'FFMPEG_BIN', 'ffmpeg')
printer(f'DEBUG: FFMPEG: {repr(FFMPEG)}.')
import os
import shutil
import sys

from mykit.kit.utils import printer

## Make all folders under repo root directory importable
_REPO_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
printer(f'DEBUG: Appending {repr(_REPO_ROOT_DIR)} to `sys.path`.')
sys.path.append(_REPO_ROOT_DIR)

from tweet_mandelbrot.constants import ARCHIVE_DIR, DRAFT_DIR


def main():

    img = os.path.join(DRAFT_DIR, 'result.png')
    printer(f'INFO: Deleting {repr(img)}.')
    os.remove(img)

    metadata_file_name = [f for f in os.listdir(DRAFT_DIR) if f.endswith('.txt')][0]
    metadata_file_path = os.path.join(DRAFT_DIR, metadata_file_name)
    src = metadata_file_path
    dst = os.path.join(ARCHIVE_DIR, metadata_file_name)
    if os.path.exists(dst): raise FileExistsError(f'Already exists: {repr(dst)}.')
    printer(f'INFO: Moving {repr(src)} to {repr(dst)}.')
    shutil.move(src, dst)


if __name__ == '__main__':
    main()
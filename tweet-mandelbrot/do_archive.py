import os
import shutil

from mykit.kit.utils import printer

from utils.constants import PROJECT_ROOT_DIR


DRAFT_DIR   = os.path.join(PROJECT_ROOT_DIR, 'tweet-mandelbrot', 'drafts')
ARCHIVE_DIR = os.path.join(PROJECT_ROOT_DIR, 'tweet-mandelbrot', 'archive')


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
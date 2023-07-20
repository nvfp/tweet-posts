import os
import shutil

from mykit.kit.utils import printer

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
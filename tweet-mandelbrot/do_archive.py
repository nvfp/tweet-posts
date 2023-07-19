import os
import shutil

from mykit.kit.utils import printer


PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():

    img = os.path.join(PROJECT_ROOT_DIR, 'drafts', 'result.png')
    printer(f'INFO: Deleting {repr(img)}.')
    os.remove(img)

    metadata_file_path = [f for f in os.listdir(os.path.join(PROJECT_ROOT_DIR, 'drafts')) if f.endswith('.txt')][0]
    metadata_file_name = os.path.basename(metadata_file_path)
    src = metadata_file_path
    dst = os.path.join(PROJECT_ROOT_DIR, 'archive', metadata_file_name)
    if os.path.exists(dst): raise FileExistsError(f'Already exists: {repr(dst)}.')
    printer(f'INFO: Moving {repr(src)} to {repr(dst)}.')
    shutil.move(src, dst)


if __name__ == '__main__':
    main()
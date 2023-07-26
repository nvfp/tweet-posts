import os
import shutil


ROOT = os.path.dirname(os.path.abspath(__file__))
METADATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '__archive_temp_dir__')
print(f'DEBUG: ROOT: {repr(ROOT)}.')
print(f'DEBUG: METADATA: {repr(METADATA)}.')


if __name__ == '__main__':

    num_archive_dirs = len(os.listdir(ROOT))
    print(f'DEBUG: num_archive_dirs: {num_archive_dirs}')

    target = os.path.join(ROOT, f'archive-{num_archive_dirs-1}')
    print(f'DEBUG: target: {repr(target)}.')

    num_files = len(os.listdir(target))
    print(f'DEBUG: num_files: {num_files}')
    if num_files == 1000:
        new_target = os.path.join(ROOT, f'archive-{num_archive_dirs}')
        print(f'INFO: Creating new archive dir {repr(new_target)}.')
        if os.path.exists(new_target): raise AssertionError(f'Already exists: {repr(new_target)}.')
        os.mkdir(new_target)
        target = new_target

    md = os.path.join(METADATA, os.listdir(METADATA)[0])
    print(f'DEBUG: md: {repr(md)}.')

    shutil.move(md, target)
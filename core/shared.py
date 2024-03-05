import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))  # project root folder

FFMPEG = os.path.join(ROOT_DIR, 'THE_VENV_CACHE', 'FFMPEG_BIN', 'ffmpeg')  # Make sure the venv cache folder name matches the one in the workflows.

RENDERED_IMG_PTH = os.path.join(ROOT_DIR, '__the_rendered_img.jpg')  # Knowing that each fractal workflow runs in a different VM, so they shouldn't overlap (overwriting one another).
if os.path.exists(RENDERED_IMG_PTH): raise AssertionError(f"UNEXPECTED: Already exists: {repr(RENDERED_IMG_PTH)}.")

RENDERED_IMG_PTH2 = os.path.join(ROOT_DIR, '__the_rendered_img2.png')

METADATA_TMP_DIR = os.path.join(os.path.dirname(ROOT_DIR), '__metadata_temp_dir__')  # to store the metadata file temporarily before committing in the metadata branch
if os.path.exists(METADATA_TMP_DIR):
    raise AssertionError(f"UNEXPECTED: Already exists: {repr(METADATA_TMP_DIR)}.")
else:
    print(f"INFO: Creating the md temp dir: {METADATA_TMP_DIR}")
    os.mkdir(METADATA_TMP_DIR)

IMG_RES = [1920, 1080]  # the output rendered resolution

#!/bin/bash
set -e  # Exit the script immediately if any command exits with a non-zero status


echo "::group::Archiving"

# Delete the image
img_path="$(pwd)/tweet_mandelbrot/draft/result.png"
echo "INFO: Deleting '$img_path'."
rm img_path

# 
file_name="$(date +%s | awk '{printf "%011d\n", $1}')-${{ steps.tweet.outputs.tweet_id }}.txt"


echo "::endgroup::"

    # metadata_file_name = [f for f in os.listdir(DRAFT_DIR) if f.endswith('.txt')][0]
    # metadata_file_path = os.path.join(DRAFT_DIR, metadata_file_name)
    # src = metadata_file_path
    # dst = os.path.join(ARCHIVE_DIR, metadata_file_name)
    # if os.path.exists(dst): raise FileExistsError(f'Already exists: {repr(dst)}.')
    # printer(f'INFO: Moving {repr(src)} to {repr(dst)}.')
    # shutil.move(src, dst)

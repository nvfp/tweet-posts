#!/bin/bash
set -e  # Exit the script immediately if any command exits with a non-zero status


echo "::group::Archiving"

# Delete the image
img_path="$(pwd)/tweet_mandelbrot/draft/result.png"
echo "INFO: Deleting '$img_path'."
# rm img_path

# Move the metadata
src="$(pwd)/tweet_mandelbrot/draft/metadata.txt"
dst="$(pwd)/tweet_mandelbrot/archive/$(date +%s | awk '{printf "%011d\n", $1}')-$TWEET_ID.txt"
echo "DEBUG: src: '$src'."
echo "DEBUG: dst: '$dst'."

echo "::endgroup::"
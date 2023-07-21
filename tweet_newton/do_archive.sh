#!/bin/bash
set -e  # Exit the script immediately if any command exits with a non-zero status


echo "::group::Archiving"

# Delete the image
img_path="$(pwd)/tweet_newton/draft/result.png"
echo "INFO: Deleting '$img_path'."
rm "$img_path"

# Metadata
src="$(pwd)/tweet_newton/draft/metadata.txt"
dst="$(pwd)/tweet_newton/archive/$(date +%s | awk '{printf "%011d\n", $1}')-$TWEET_ID.txt"
echo "DEBUG: src: '$src'."
echo "DEBUG: dst: '$dst'."

# Change the tweet_id value in metadata.txt
sed -i "s/tweet_id: .*/tweet_id: $TWEET_ID/" "$src"

# Check if the destination already exists or not
if [ -e "$dst" ]; then
    echo "ERROR: File '$dst' already exists."
    exit 1
fi

# Move the metadata file
echo "INFO: Moving src -> dst."
mv "$src" "$dst"

echo "::endgroup::"
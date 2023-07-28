#!/bin/bash
set -e  # Exit the script immediately if any command exits with a non-zero status


echo "::group::Debugging purposes"
echo "pwd: '$(pwd)'"
echo "GITHUB_WORKSPACE: '$GITHUB_WORKSPACE'"
echo "VENV_CACHE_DIR_NAME: '$VENV_CACHE_DIR_NAME'"
echo "::endgroup::"


# Check
if [ -d "$GITHUB_WORKSPACE/$VENV_CACHE_DIR_NAME" ]; then
    echo "ERROR: VENV cache directory '$GITHUB_WORKSPACE/$VENV_CACHE_DIR_NAME' already exists."
    exit 1
fi

# Create new VENV
python -m venv $VENV_CACHE_DIR_NAME
echo "++ after creating venv ++"
ls
echo "---"
echo "++ VENV_CACHE_DIR_NAME ++"
ls $VENV_CACHE_DIR_NAME
echo "---"

# Activate py venv
source $GITHUB_WORKSPACE/$VENV_CACHE_DIR_NAME/bin/activate
echo "INFO: which python: '$(which python)'"

echo "::group::pip list (before)"
pip list
echo "::endgroup::"

echo "::group::Install Python dependencies"
pip install numba==0.55.2 numpy==1.22.4 mykit==6.0.0 tweepy openai
echo "::endgroup::"

echo "::group::pip list (after)"
pip list
echo "::endgroup::"

cd $VENV_CACHE_DIR_NAME
mkdir FFMPEG_EXTRACT
cd FFMPEG_EXTRACT

## Ref: https://ffmpeg.org/download.html#LinuxBuilds https://johnvansickle.com/ffmpeg/
echo "::group::Download ffmpeg"
sudo wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
sudo wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz.md5
echo "::endgroup::"

# Verify the MD5 checksum
md5sum -c ffmpeg-release-amd64-static.tar.xz.md5

# Check if the MD5 verification was successful before proceeding
if [ $? -ne 0 ]; then
    echo "ERROR: FFmpeg MD5 checksum verification failed. Aborting installation."
    exit 1
fi

echo "::group::Extract the static build from the archive"
sudo tar xvf ffmpeg-release-amd64-static.tar.xz
echo "::endgroup::"

# Move it
sudo mv ffmpeg-*-static $GITHUB_WORKSPACE/$VENV_CACHE_DIR_NAME/FFMPEG_BIN

# Remove the extract folder
rm -r $GITHUB_WORKSPACE/$VENV_CACHE_DIR_NAME/FFMPEG_EXTRACT


echo "::group::Debugging purposes"

echo "-+ GITHUB_WORKSPACE -+"
ls $GITHUB_WORKSPACE
echo "-+-+"

echo "-+ GITHUB_WORKSPACE/VENV_CACHE_DIR_NAME -+"
ls $GITHUB_WORKSPACE/$VENV_CACHE_DIR_NAME
echo "-+-+"

echo "-+ GITHUB_WORKSPACE/VENV_CACHE_DIR_NAME/FFMPEG_BIN -+"
ls $GITHUB_WORKSPACE/$VENV_CACHE_DIR_NAME/FFMPEG_BIN
echo "-+-+"

echo "::endgroup::"
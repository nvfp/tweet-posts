import os

from mykit.kit.utils import printer

from utils.constants import REPO_ROOT_DIR


ARCHIVE_DIR = os.path.join(REPO_ROOT_DIR, 'tweet_phoenix', 'archive')
DRAFT_DIR   = os.path.join(REPO_ROOT_DIR, 'tweet_phoenix', 'draft')
printer(f'DEBUG: ARCHIVE_DIR: {repr(ARCHIVE_DIR)}.')
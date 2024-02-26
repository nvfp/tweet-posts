import os, string
from datetime import datetime, timezone, timedelta
from .shared import METADATA_TMP_DIR

def process_post_desc(post_desc):
    out = ''
    for c in post_desc:
        if c.lower() in 'abcdefghijklmnopqrstuvwxyz0123456789':
            out += c
            if len(out) > 17: break
    return out

def write_metadata_file(fractal_name, tweet_id, masto_id, post_desc, pack_metadata:dict):
    file_pth = os.path.join(
        METADATA_TMP_DIR,
        datetime.now().astimezone(timezone(timedelta(hours=0))).strftime(
            f"%Y%m%d_%H%M%S_utc%z_{fractal_name}_{process_post_desc(post_desc)}_{tweet_id}_{masto_id}.txt"
        )
    )
    text = ''
    for key, val in pack_metadata.items():
        text += f"{repr(key)}: {repr(val)}\n"
    
    if os.path.exists(file_pth): raise AssertionError(f"Already exists: {repr(file_pth)}")
    with open(file_pth, 'w') as f:
        f.write(text)

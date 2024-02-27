import os, shutil

def main():
    root = os.path.dirname(__file__)
    tmp_dir = os.path.join(os.path.dirname(root), '__metadata_temp_dir__')
    file_pth = os.path.join(tmp_dir, os.listdir(tmp_dir)[0])

    k = len(os.listdir(root)) - 2  # exclude .git folder too
    target = os.path.join(root, f"pack_{str(k).zfill(3)}")
    
    if len(os.listdir(target)) > 2500:
        target = os.path.join(root, f"pack_{str(k+1).zfill(3)}")
        os.mkdir(target)

    shutil.move(file_pth, target)

if __name__ == '__main__':
    main()

import sys

def get_fractal_name():
    args = sys.argv
    if len(args) != 2: raise AssertionError(f"Need 1 positional arg, the fractal name.")
    return args[1]

def main():
    pass

if __name__ == '__main__':
    main()

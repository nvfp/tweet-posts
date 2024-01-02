import random


def get_list():
    return [
        '#AI',
        '#MachineLearning',
        '#DeepLearning',
        '#Mathematics',
        '#Nature',
        '#Fractals',
        '#Art',
        '#DigitalArt',
        '#VisualArt',
        "#GenerativeArt",
    ]


def get_random_hashtag(num):
    out = []
    while len(out) < num:
        h = random.choice(get_list())
        if h in out: continue
        out.append(h)
    return out

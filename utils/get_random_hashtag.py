import random


def get_list():
    return [
        '#Physics',
        '#Fractals',
        '#Biology',
        '#Education',
        '#DataScience',
        '#Science',
        '#Astronomy',
        '#MachineLearning',
        '#MathEducation',
        '#Learning',
        '#Math',
        '#Teaching',
        '#EdTech',
        '#ScienceEducation',
        '#STEM',
    ]


def get_random_hashtag(num):
    out = []
    while len(out) < num:
        h = random.choice(get_list())
        if h in out: continue
        out.append(h)
    return out
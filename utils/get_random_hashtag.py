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


def get_random_hashtag():
    ht1 = random.choice(get_list())
    ht2 = random.choice(get_list())
    while ht2 == ht1: ht2 = random.choice(get_list())
    return ht1, ht2
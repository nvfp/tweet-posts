import random


def get_list():
    return [
        '#ArtificialIntelligence',
        '#MachineLearning',
        '#DeepLearning',
        '#NeuralNetworks',
        '#ComputerVision',
        '#NaturalLanguageProcessing',
        '#Robotics',
        '#DataScience',
        '#AIResearch',
        '#AutonomousSystems',
        '#AIProgramming',
        '#AIEthics',
        '#AIInnovation',
        '#AIApplications',
        '#AIAlgorithms',
    ]


def get_random_hashtag(num):
    out = []
    while len(out) < num:
        h = random.choice(get_list())
        if h in out: continue
        out.append(h)
    return out
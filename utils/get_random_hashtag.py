import random


def get_list():
    return [
        '#Mandelbrot',
        '#Fractals',
        '#MathArt',
        '#Mathematics',
        '#ArtOfTheDay',
        '#AlgorithmArt',
        '#ComplexNumbers',
        '#Infinity',
        '#GeometricArt',
        '#RecursiveArt',
        '#ChaosTheory',
        '#MathBeauty',
        '#FractalArt',
        '#ArtInMath',
        '#DigitalArt',
        '#MathArtGallery',
        '#PatternArt',
        '#FractalLove',
        '#Nature',
        '#Science',
        '#Art',
        '#Patterns',
        '#MathematicalArt',
        '#Symmetry',
        '#AlgorithmicArt',
        '#AbstractArt',
        '#MathematicalBeauty',
        '#Geometry',
        '#Fibonacci',
        '#GoldenRatio',
        '#MathematicalPatterns',
        '#MathLovers',
        '#CreativeCoding',
        '#VisualArt',
        '#MathInspiration',
        '#BeautyOfMath',
        '#MathematicalDesign',
    ]


def get_random_hashtag():
    ht1 = random.choice(get_list())
    ht2 = random.choice(get_list())
    while ht2 == ht1: ht2 = random.choice(get_list())
    return ht1, ht2
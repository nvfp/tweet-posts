import unittest

from utils.get_random_fractal_greeting import _get_list as greeting_list
from utils.get_random_hashtag import get_list as hashtag_list


class TestDuplicate(unittest.TestCase):

    def test_no_duplicate_greetings(self):
        the_list = greeting_list('foo', 'bar')
        self.assertEqual(len(set(the_list)), len(the_list))

    def test_no_duplicate_hashtag(self):
        the_list = hashtag_list()
        self.assertEqual(len(set(the_list)), len(the_list))


if __name__ == '__main__':
    unittest.main()
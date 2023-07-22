import unittest

from utils.get_random_fractal_greeting import _get_list


class TestDuplicate(unittest.TestCase):

    def test_no_duplicate_greetings(self):
        random_greetings = _get_list('foo', 'bar')
        self.assertEqual(len(set(random_greetings)), len(random_greetings))


if __name__ == '__main__':
    unittest.main()
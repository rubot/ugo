import unittest


class TestBootFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_shuffle(self):
        self.seq.sort()
        self.assertEqual(self.seq, range(10))


if __name__ == '__main__':
    unittest.main()

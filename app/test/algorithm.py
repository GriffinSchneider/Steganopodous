import unittest
from .. import algorithm

class AlgorithmTest(unittest.TestCase):

  def test_encode_decode(self):
    self.assertEqual(0, algorithm.decode(algorithm.encode(0, 100)))
    self.assertEqual(1, algorithm.decode(algorithm.encode(1, 100)))
    self.assertEqual(0, algorithm.decode(algorithm.encode(0, 10000000)))
    self.assertEqual(1, algorithm.decode(algorithm.encode(1, 10000000)))

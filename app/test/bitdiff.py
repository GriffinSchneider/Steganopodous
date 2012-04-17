import unittest
import StringIO
from .. import bitdiff

class BitdiffTest(unittest.TestCase):
	
  def test_compare(self):
    file1 = open("app/test/data/bitdiff/file1")
    file1_2 = open("app/test/data/bitdiff/file1")
    file2 = open("app/test/data/bitdiff/file2") 
    self.assertEqual(1.0, bitdiff.compare(file1,file1_2))
    file1.seek(0)
    self.assertEqual(95.0/96.0, bitdiff.compare(file1,file2))
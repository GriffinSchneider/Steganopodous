import unittest
import StringIO
import tempfile
from .. import bitdiff
from ..bitstream import BitStream

class BitStreamTest(unittest.TestCase):
	
  def test_read(self):
    file1 = BitStream(open('app/test/data/bitdiff/file1', 'rb'))
    self.assertEqual(0, file1.read())
    self.assertEqual(1, file1.read())
    self.assertEqual(0, file1.read())
    
  def test_write(self):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file2 = tempfile.NamedTemporaryFile(delete=False)
    temp_file2.write("H")
    bs = BitStream(temp_file)
    bs.write(0)
    bs.write(1)
    bs.write(0)
    bs.write(0)
    bs.write(1)
    bs.write(0)
    bs.write(0)
    bs.write(0)
    bs.close()
    temp_file.close()
    temp_file2.close()
    self.assertEqual(1.0, bitdiff.compare(open(temp_file.name),open(temp_file2.name)))
    
  def test_iterate(self):
    self.assertEqual(1.0, 1.0)
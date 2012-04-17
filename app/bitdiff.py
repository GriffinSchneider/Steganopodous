#!/usr/bin/env python

from bitstream import BitStream
import sys

def compare(file1, file2):
  stream1 = BitStream(file1) 
  stream2 = BitStream(file2) 
  
  n_same = 0
  n_different = 0
  for bit1, bit2 in zip(stream1, stream2):
    if (bit1 is None or bit2 is None):
      break
    
    if bit1 == bit2:
      n_same += 1
    else:
      n_different += 1
      
  return 1.0*n_same/(n_different+n_same)

if __name__ == "__main__":
  print compare(open(sys.argv[1]), open(sys.argv[2]))

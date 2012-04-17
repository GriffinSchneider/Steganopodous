#!/usr/bin/env python

import unittest
import app.test.algorithm
import app.test.bitdiff
import app.test.bitstream
import app.test.audiofile

if __name__ == '__main__':
  tests = [app.test.algorithm.AlgorithmTest,app.test.bitdiff.BitdiffTest,app.test.bitstream.BitStreamTest,app.test.audiofile.AudioFileTest]
  suites = [unittest.TestLoader().loadTestsFromTestCase(test) for test in tests]
  main_suite = unittest.TestSuite(suites)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(main_suite)

import unittest
import StringIO
import tempfile
from ..audio.audiofile import AudioFile
from ..audio.audiofile import FormatError

class AudioFileTest(unittest.TestCase):
	
  def test_open(self):
    file1 = AudioFile.open('app/test/data/audio/Hewlett.isaMP3file')
    self.assertEqual("mp3", file1.get_format())
    file2 = AudioFile.open('app/test/data/audio/Hewlett.thisisawavfile')
    self.assertEqual("wav", file2.get_format())
    file3 = AudioFile.open('app/test/data/audio/tags.mp3')
    self.assertEqual("mp3", file3.get_format())
    self.assertRaises(FormatError, AudioFile.open, ('app/test/data/message/bitdiff.py'))
    self.assertRaises(IOError, AudioFile.open, ('app/test/data/message/bogus.py'))
    
  def test_get_n_channels(self):
    file1 = AudioFile.open('app/test/data/audio/Hewlett.isaMP3file')
    self.assertEqual(2, file1.get_n_channels())
    file2 = AudioFile.open('app/test/data/audio/Hewlett.thisisawavfile')
    self.assertEqual(2, file2.get_n_channels())
    file3 = AudioFile.open('app/test/data/audio/tags.mp3')
    self.assertEqual(2, file3.get_n_channels())
    
  def test_get_n_frames(self):
    file1 = AudioFile.open('app/test/data/audio/Hewlett.isaMP3file')
    file2 = AudioFile.open('app/test/data/audio/Hewlett.thisisawavfile')
    self.assertEqual(file1.get_n_frames(), file2.get_n_frames())
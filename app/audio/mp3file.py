from audiofile import AudioFile
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import tempfile
import wave
import subprocess
import os
import shutil

DEFAULT_BITRATE = 128000
LAME_PATH = "/course/cs4500wc/bin/lame"
NULL_FP = open(os.devnull, 'w')

# Uses WAV as a canonical format and delgates to the wave module until
# closed.

class MP3File(AudioFile):
  
  def __init__(self, filename, is_write):
    self.is_write = is_write      
    self.filename = filename

    # Create a temporary WAV file and get its name
    temp_file = tempfile.NamedTemporaryFile(delete = False)
    self.temp_name = temp_file.name
    temp_file.close()
    
    if self.is_write:
      # If we're writing, write to the temporary WAV file
      try:
        self.wave = wave.open(self.temp_name, 'w')
      except:
        sys.stderr.write("Failed to create temporary file: "  + self.temp_name)
        exit()
      self.bitrate = DEFAULT_BITRATE
      self.id3 = {}
    else:
      # lame requires the file to have a .mp3 suffix, so copy the
      # input file to a new file with a .mp3 suffix before running it
      # through lame.
      temp_input_copy = tempfile.NamedTemporaryFile(delete = False, suffix = ".mp3")
      temp_input_copy_name = temp_input_copy.name
      temp_input_copy.close()
      shutil.copy(self.filename, temp_input_copy_name)
      
      # If we're reading, use lame to decode the input MP3 into the
      # temporary WAV file and then read from it
      subprocess.check_call([LAME_PATH, "--decode", temp_input_copy_name, self.temp_name], 
                            stdout=NULL_FP, 
                            stderr=NULL_FP)
     
      os.remove(temp_input_copy_name)
      try:
        self.wave = wave.open(self.temp_name, 'r')
      except:
        sys.stderr.write("Failed to create temporary file: "  + self.temp_name)
        exit()
      mp3 =  MP3(filename, ID3 = EasyID3)
      self.bitrate = mp3.info.bitrate
      self.id3 = mp3.tags
      
  def get_params(self):
    return [self.bitrate, self.wave.getparams(), self.id3]
      
  def set_params(self, params):
    self.bitrate = params[0]
    self.wave.setparams(params[1])
    self.id3 = params[2]
    
  def close(self):
    self.wave.close()
    
    if self.is_write:
      # Now that we're done writing, use lame to encode the temporary
      # WAV file into our output MP3
      subprocess.check_call([LAME_PATH, "-b", str(self.bitrate/1000), 
                              self.temp_name, self.filename], 
                            stdout=NULL_FP,  
                            stderr = NULL_FP)
      if (self.id3 is not None):
        # Write ID3 tags to output
        mp3 = MP3(self.filename, ID3 = EasyID3)
        # From http://code.google.com/p/mutagen/issues/detail?id=64
        try:
          mp3.add_tags(ID3=EasyID3)
        except:
          pass
        for key, val in self.id3.items():
          mp3[key] = val
        mp3.save()
      os.remove(self.temp_name)
    
  def get_format(self):
    return "mp3"

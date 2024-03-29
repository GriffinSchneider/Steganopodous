from audiofile import AudioFile
import wave

class WavFile(AudioFile):
    
  def __init__(self, filename, is_write):
    if is_write:
      self.wave = wave.open(filename, 'w')
    else:
      self.wave = wave.open(filename, 'r')
  
  def get_params(self):
    return self.wave.getparams()
      
  def set_params(self, params):
    self.wave.setparams(params)
    
  def close(self):
    self.wave.close()
    
  def get_format(self):
    return "wav"
    

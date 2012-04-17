from mutagen.mp3 import MP3
import numpy as np
import sndhdr

class AudioFile:
    
  @classmethod
  def open(cls, filename, write_type = None):
    """ 
    Open an audio file. write_type is "wav" or "mp3", if
    writing. Automatically determines the file format if reading.
    """
    from wavfile import WavFile
    from mp3file import MP3File
    
    if (write_type == None):
      file_object = open(filename, "rb")
      try:
        layer = MP3(filename).info.layer
      except:
        layer = -1
      if (layer == 3):
        return MP3File(filename, False)
      elif ((sndhdr.what(filename) or [None])[0] == "wav"):
        return WavFile(filename, False)
      else:
        raise FormatError("unrecognized audio format")
        exit()
      
    else:
      if (write_type == "wav"):
        return WavFile(filename, True)
      elif (write_type == "mp3"):
        return MP3File(filename, True)
      else:
        assert False
    
  def read_sectors(self, sector_size):
    """ 
    Read the file by sector, as determined by sector_size (in
    frames). A sector is an array of channels, each of which is an
    array of magnitudes. Returns a tuple containing a generator for
    the sectors and the number of frames not covered by the generator.
    """
    in_n_sectors, in_n_extra_frames = divmod(self.get_n_frames(), sector_size)
    return (self.__read_sectors_generator(sector_size, in_n_sectors), in_n_extra_frames)

  def __read_sectors_generator(self, sector_size, in_n_sectors): 
    for _ in range(0, in_n_sectors):
      # Create an array of samples from the current sector of the input
      #  audio file.
      sector_frames = np.fromstring(self.read_frames(sector_size), np.int16)
      # Split the array into channels; 'F' = FORTRAN (column-major) order.
      #  Ex: [L1 R1 L2 R2] -> [[L1, L2], [R1, R2]]
      yield np.reshape(sector_frames, (self.get_n_channels(), -1), 'F')

  def write_sector(self, sector):
    """ See read_sectors """
    # Combine all channels into a single array; 'F' = FORTRAN order.
    #  Ex: [[L1, L2], [R1, R2]] -> [L1 R1 L2 R2]
    # Then, write to the output WAV file.
    self.write_frames(np.reshape(sector, (1, -1), 'F').tostring())

  def get_n_channels(self):
    return self.wave.getnchannels()
  
  def get_n_frames(self):
    return self.wave.getnframes()
  
  def write_frames(self, frames):
    self.wave.writeframes(frames)
    
  def read_frames(self, n_frames):
    return self.wave.readframes(n_frames)

class FormatError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

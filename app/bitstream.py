class BitStream():
  """File wrapper to allow reading/writing bytes a single bit at a time"""

  def __init__(self, file):
    """Inits a BitStream wrapper around a given file."""
    self.file = file
    self.write_buff, self.write_bit = bytearray(1), 0
    self.read_buff, self.read_bit = bytearray(1), 0

  def write(self, bit):
    """Write a single bit to the wrapped file (not always immediately)."""
    self.write_buff[0] = (self.write_buff[0] << 1 | bit) & 0xff
    is_buffer_full, self.write_bit = divmod(self.write_bit + 1, 8)
    if is_buffer_full: self.file.write(self.write_buff)

  def close(self):
    """Output any remaining data (0-padded to nearest byte) and close file."""
    for _ in range(self.write_bit, 8 * (self.write_bit > 0)): self.write(0)
    self.file.close()

  def read(self):
    """Read the next bit from the output file (or None if EOF)"""
    if self.read_bit==0 and not self.file.readinto(self.read_buff): return None
    self.read_bit = (self.read_bit + 1) % 8
    return self.read_buff[0] >> (7 - ((self.read_bit - 1) % 8)) & 1
  
  def next(self):
    """Read the next bit per the Python Iterable contract"""
    bit = self.read()
    if bit is None: raise StopIteration
    return bit

  def __iter__(self):
    """Support Iterable interface for clean file reading with 'for' loops"""
    return self

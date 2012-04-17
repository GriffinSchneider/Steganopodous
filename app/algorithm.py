AMP = 150000#300000

# We are using amplitude-shift keying modulation with a bit
# represented as either a high (1) or low (0) amplitude at a specific
# (pseudorandomly chosen) frequency.

def decode(fft_val):
  """ Decode a single bit """
  # Check the carrier audio to see if a 0 or 1 bit was encoded
  return abs(fft_val) > AMP/2

def encode(bit, fft_val):
  """ Encode a single bit into a single frequency. """
  amp = max(AMP, abs(fft_val)) if bit else 0
  if (fft_val == 0): fft_val = 1
  # Obtain a unit vector to maintain phase
  return fft_val / abs(fft_val) * amp



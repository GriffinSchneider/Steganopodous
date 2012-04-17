#!/usr/bin/env python

import app.bitdiff as bitdiff
import os
import itertools
import tempfile
import subprocess

AUDIO_DIR = "app/test/data/audio/"
MESSAGE_DIR = "app/test/data/message/"

if __name__ == "__main__":
    
   temp_file = tempfile.NamedTemporaryFile(delete = False)
   encoded_audio_name = temp_file.name
   temp_file.close

   temp_file = tempfile.NamedTemporaryFile(delete = False)
   decoded_message_name = temp_file.name
   temp_file.close

   audio_file_names = os.listdir(AUDIO_DIR)
   message_file_names = os.listdir(MESSAGE_DIR)
   
   for audio_file_name in audio_file_names:
     for message_file_name in message_file_names:
       subprocess.check_call(["./stegan", "--encode", AUDIO_DIR+audio_file_name, 
                               MESSAGE_DIR+message_file_name, encoded_audio_name])
       subprocess.check_call(["./stegan", "--decode", encoded_audio_name, decoded_message_name])
       original = open(MESSAGE_DIR+message_file_name)
       decoded = open(decoded_message_name)
       print audio_file_name, message_file_name, bitdiff.compare(original, decoded)
       original.close()
       decoded.close()
       
   os.remove(encoded_audio_name)
   os.remove(decoded_message_name)
    

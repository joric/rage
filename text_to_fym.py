#!/bin/python3

# ayumi text to fym converter
# Author: Joric, https://github.com/joric
# tags: ayumi, psg2ym

import sys
import struct
import zlib

frame_data = []

Header_template = {
  'pan_a': 10,
  'pan_b': 50,
  'pan_c': 90,
  'volume': 50
}

def save_fym(name, header, frame_data):
    data = bytearray()

    data.extend(struct.pack('i', 22)) # offset to data
    data.extend(struct.pack('i', len(frame_data))) # frame count
    data.extend(struct.pack('i', 0)) # loop frame
    data.extend(struct.pack('i', 1750000)) # clock rate
    data.extend(struct.pack('i', 50)) # frame rate
    data.extend(struct.pack('B', 0)) # track name
    data.extend(struct.pack('B', 0)) # author name

    # frame data is transposed
    for j in range(14):
        for i in range(len(frame_data)):
            data.extend(struct.pack('B', frame_data[i][j]))

    if '.fym' in name:
        data = zlib.compress(data, 9)
    f = open(name, 'wb')
    f.write(data)
    f.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
      print('text_to_fym input.text output.fym')
      sys.exit(0)

    filename = sys.argv[1]

    f = open(filename, 'r')
    file_data = f.read()
    f.close()

    lines = file_data.splitlines()
    frame_count = 0
    mode = 0
    header = Header_template

    for l in lines:
        if mode==0 and 'frame_count' in l:
            frame_count = int(l.split(' ')[1])
        elif mode==0 and 'frame_data' in l:
           mode = 1
        elif mode==1:
            frame_data.append([int(x) for x in l.split(' ')])

    save_fym(sys.argv[2], header, frame_data)

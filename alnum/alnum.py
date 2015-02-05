#!/usr/bin/python2

# alnum_encoder.py
# from: http://inaz2.hatenablog.com/entry/2014/07/13/025626


# decomposite.py
import sys
import struct

word = int(sys.argv[1], 16)

allowed = range(0x30, 0x3a) + range(0x41, 0x5b) + range(0x61, 0x7b)
# no "binsh" or "BINSH"
for c in [ ord(_) for _ in "binshBINSH" ]:
    allowed.remove(c)

chunk = struct.pack('<I', word)
x = ''
y = ''
z = ''

for c in map(ord, chunk):
    if c >= 0x80:
        z += '\xff'
        c ^= 0xff
    else:
        z += '\x00'
    for i in allowed:
        if i^c in allowed:
            x += chr(i)
            y += chr(i^c)
            break

print hex(struct.unpack('<I', x)[0])
print hex(struct.unpack('<I', y)[0])
print hex(struct.unpack('<I', z)[0])



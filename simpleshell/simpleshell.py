#!/usr/bin/env python

import struct
from socket import *
import telnetlib
import re

ip = 'secprog.cs.nctu.edu.tw'
port = 10012

soc = socket(AF_INET, SOCK_STREAM)
soc.connect((ip,port))
data = soc.recv(4096)

# get time from info
payload = b"info\n"
soc.send(payload)
data = soc.recv(4096)
print(data)
data = soc.recv(4096)
print(data)

# get time
m = re.search('141(\d+)', data.decode())
print("get")
seed = int(m.group(0))
print(seed)

# gen passcode
x1 = 65535 * seed + 31337
x1 &= 0xff

x2 = seed // 65535
x2 &= 0xff

key = "DoYouThinkThisIsPassword"
passcode = []
cnt = 0
for cnt in range(0, 24, 4):
    passcode.append(ord(key[cnt]) ^ x1)
    passcode.append(ord(key[cnt+1]))
    passcode.append(ord(key[cnt+2]) ^ x2)
    passcode.append(ord(key[cnt+3]))

# login as admin
payload = b"login\n"
soc.send(payload)
data = soc.recv(2048)
print(data)

payload = b"admin\n"
soc.send(payload)
data = soc.recv(2048)
print(data)

# send passocde
soc.send((("".join([chr(c) for c in passcode])) + "\n").encode())
data = soc.recv(2048)
print(data)

# cat flag
payload = b"flag\n"
soc.send(payload)
data = soc.recv(2048)
print(data)



payload = b"exit\n"
soc.send(payload)

# get interactive shell
#t = telnetlib.Telnet()
#t.sock = soc
#t.interact()


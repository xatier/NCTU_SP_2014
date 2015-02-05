# Write up: Simpleshell (1-2)

## ymli (0016045)


### try to nc to it, need to login as a admin and use flag command to cat the flag

### try to write a gdb script generator to guess the encryption algorithm

    - gen.py [1]
    - the seed is the time
    - xor with a string "blahblahblah" + "anonymous" (?

### try to understand the assembly code

    - the encryption algorithm is just a simple math tricks,
      try to read the assembly code and figure out the math form
    - use different tools to decompile the assembly code

        [Imgur](http://i.imgur.com/I60LnNR.png)
        [Imgur](http://i.imgur.com/zqMQgX1.png)

        http://pastebin.com/Hh6fvcgL

### write the exploit script [2]

    - simpleshell.py
    - use `info` command to get time (seed)
    - generate the passcode
    - login as admin
    - use `flag` command to get the flag

----

## Appeldix

### [1] gen.py

```python
#!/usr/bin/env python

import sys
import os

#f = open("script.gdb", "w")
#gdb_script = """
#set logging file gdb_out
#set logging overwrite off
#set verbose off
#set confirm off
#b *0x08048a63
#r <  test
#set logging on
#print "======="
#x/20x $ebp - 0x54
#x/s $ebp - 0x54
#set logging off
#quit
#"""
#f.write(gdb_script)
#f.close()

f = open("test", "w")
f.write("login\n")
f.write("admin\n")
f.write(chr(0x56)*20)
f.close()


exec_gdb = "gdb -q simpleshell -x script.gdb"
os.system(exec_gdb)
```


### [2] simpleshell.py

```python
#!/usr/bin/env python

import struct
from socket import *
import telnetlib
import re

ip = 'secprog.cs.nctu.edu.tw'
port = 10001

soc = socket(AF_INET, SOCK_STREAM)
soc.connect((ip,port))
data = soc.recv(4096)

# get time from info
payload = b"info\n"
soc.send(payload)
data = soc.recv(4096)
data = soc.recv(4096)

# get time
m = re.search('1412(\d+)', data.decode())
print("get")
seed = int(m.group(0))

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
```

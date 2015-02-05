#include <stdio.h>
#include <stdlib.h>
#include <time.h>


int main (void) {
    int i;
    // for  i = 0; (signed int)(v3 - 1) > i; i += 4 )
    // {
    //     s[i] ^= dword_804A548;
    //     s[i + 2] ^= (signed int)seed / 65535;
    // }
    //
    char s[] = "DoYouThinkThisIsPassword";
    char p[] = "\x00\x00\x00\x00anonymous";

    unsigned int seed = time(0);
    seed = 65535 * seed + 31337;
    for (i = 0; i < 32; i++)
        printf("%x ", seed >> (31-i) & 0xff);


   // for (i = 0; i < ) {



    // 1 3 6 c 18 31 63 c6 8d 1a 34 69 d2 a4 49 92 24 49 92 25 4b 97 2f 5f bf 7e fd fa f5 ea d5 aa
    // 1 3 6 c 18 31 63 c6 8d 1a 35 6a d5 ab 57 af 5e bd 7a f5 eb d7 af 5f bf 7e fc f8 f1 e3 c6 8d


//    }
    return 0;
}

// 0x804a548:      0x39    0x60    0x03    0xc6    0x30    0x1a    0x2d    0x54
// 0x804a550:      0x61    0x6e    0x6f    0x6e    0x79    0x6d    0x6f    0x75
// 0x804a558:      0x73    0x00    0x00    0x000
//
//
// 0x804a548:      0x22    0x60    0x1a    0xc6    0x47    0x1a    0x2d    0x54
// 0x804a550:      0x61    0x6e    0x6f    0x6e    0x79    0x6d    0x6f    0x75
// 0x804a558:      0x73    0x00    0x00    0x00

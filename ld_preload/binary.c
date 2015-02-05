#include<stdio.h>

main() {
    char buf[40];

    printf("What's your name? ");
    fflush(stdout);
    
    fgets(buf, 100, stdin);

    printf("Hello, %s", buf);
}

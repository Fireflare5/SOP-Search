#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "largeData.h"

int main() {
    uint2048_t a;
    uint2048_t b;
    uint2048_t c;
    init2048(&a);
    init2048(&b);
    init2048(&c);

    a.bytes[0] = 0x05;
    b.bytes[0] = 0x0E;

    c = division2048(a,b);

    for(int i = 255; i >= 0; --i) {
        for(int j = 0; j < 8; ++j) {
            if(!(j % 4)) {
                printf(" ");
            }
            printf("%c", c.bytes[i] & 0x80 ? '1' : '0');
            c.bytes[i] <<= 1;
        }
    }
    printf("\n");

    return 0;
}
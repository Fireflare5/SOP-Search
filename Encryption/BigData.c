#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "largeData.h"

int main() {
    uint2048_t a;
    uint2048_t b;
    uint4096_t c;
    init2048(&a);
    init2048(&b);
    init4096(&c);

    time_t raw_time;
    for(int i = 0; i < 256; ++i) {
        time(&raw_time);
        int x = raw_time;
        for(int j = 0; j < i * 256; ++j) {
            x = raw_time * x + 3 % 0xFF;
        }
        a.bytes[i] = x;
        for(int j = 0; j < (i - 1) * 256; ++j) {
            x = raw_time * x + 3 % 0xFF;
        }
        b.bytes[i] = x;
    }

    c = multiply2048(a,b);

    for(int i = 511; i >= 0; --i) {
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
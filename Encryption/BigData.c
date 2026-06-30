#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Custom data types
//###########################################################
typedef unsigned short int usit;

// 256bit unsigned int
typedef struct {
    unsigned char bytes[32];
} uint256_t;

void init256(uint256_t *bytes) {
    memset(bytes, 0, 32);
}

// 2048bit unsigned int
typedef struct {
    unsigned char bytes[256];
} uint2048_t;

void init2048(uint2048_t *bytes) {
    memset(bytes, 0, 256);
}

// 2048bit addition implementation
uint2048_t add2048(uint2048_t a, uint2048_t b) {
    uint2048_t basket;
    init2048(&basket);

    int j = 1;

    while(j) {

        j = 0;

        for(int i = 0; i < 256; ++i) {
            basket.bytes[i] = (a.bytes[i] & b.bytes[i]);
            a.bytes[i] ^= b.bytes[i];
        }

        for(int i = 255; i >= 0; --i) {
            basket.bytes[i] <<= 1;

            // Shifts end bit to start bit of the next byte
            if(i) {
                basket.bytes[i] ^= basket.bytes[i-1] & 0x80 ? 0x01 : 0x00;
            }

            b.bytes[i] = basket.bytes[i];

            if(b.bytes[i]) {
                j = 1;
            }
        }
    }

    return a;
}

// 4096bit unsigned int
typedef struct {
    unsigned char bytes[512];
} uint4096_t;

void init4096(uint4096_t *bytes) {
    memset(bytes, 0, 512);
}

//###########################################################

int main() {
    uint2048_t a;
    uint2048_t b;
    uint2048_t c;
    init2048(&a);
    init2048(&b);
    init2048(&c);

    a.bytes[0] = 0xFF;
    b.bytes[0] = 0xFF;
    b.bytes[1] = 0x4;

    c = add2048(a,b);

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
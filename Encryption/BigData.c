#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

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

// 4096bit unsigned int
typedef struct {
    unsigned char bytes[512];
} uint4096_t;

void init4096(uint4096_t *bytes) {
    memset(bytes, 0, 512);
}

uint4096_t add4096(uint4096_t a, uint4096_t b) {
    uint4096_t basket;
    init4096(&basket);

    int j = 1;

    while(j) {

        j = 0;

        for(int i = 0; i < 512; ++i) {
            basket.bytes[i] = (a.bytes[i] & b.bytes[i]);
            a.bytes[i] ^= b.bytes[i];
        }

        for(int i = 511; i >= 0; --i) {
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

uint4096_t multiply2048(uint2048_t ab, uint2048_t b) {
    uint4096_t out;
    init4096(&out);

    uint4096_t a;
    init4096(&a);

    int m = 0;

    for(int i = 0; i < 256; ++i) {
        a.bytes[i] = ab.bytes[i];
    }

    for(int i = 0; i < 256; ++i) {
        if(b.bytes[i]) {
            for(int j = 0; j < 8; ++j) {
                if(b.bytes[i] & 0x01) {
                    for(int k = 0; k < j + i * 8 - m; ++k) {
                        for(int l = 511; l >= 0; --l) {
                            a.bytes[l] <<= 1;

                            if(l) {
                                a.bytes[l] ^= a.bytes[l-1] & 0x80 ? 0x01 : 0x00;
                            }
                        }
                    }
                    out = add4096(out, a);
                    m = j + i * 8;
                }
                b.bytes[i] >>= 1;
            }
        }
    }

    return out;
}

//###########################################################

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
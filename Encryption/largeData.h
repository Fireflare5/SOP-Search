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

// Initialize by setting all bits in memory to zeros.
void init256(uint256_t *bytes) {
    memset(bytes, 0, 32);
}

// 4096bit unsigned int
typedef struct {
    unsigned char bytes[512];
} uint4096_t;

// Initialize by setting all bits in memory to zeros.
void init4096(uint4096_t *bytes) {
    memset(bytes, 0, 512);
}

// Add two 4096 bit numbers
// a + b = c
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

uint4096_t subtract4096(uint4096_t a, uint4096_t b) {
    uint4096_t basket;
    init4096(&basket);

    int j = 1;
    
    while(j) {

        j = 0;

        for(int i = 0; i < 512; ++i) {
            basket.bytes[i] = (~a.bytes[i]) & b.bytes[i];
            a.bytes[i] ^= b.bytes[i];
            j = basket.bytes[i] ? 1 : 0;
        }

        for(int i = 511; i >= 0; --i) {
            basket.bytes[i] <<= 1;
            basket.bytes[i] = basket.bytes[i - 1] & 0x80 && i ? 0x1 : 0x0;
        }

        b = basket;
    }
    return a;
}

// 2048bit unsigned int
typedef struct {
    unsigned char bytes[256];
} uint2048_t;

// Initialize by setting all bits in memory to zeros.
void init2048(uint2048_t *bytes) {
    memset(bytes, 0, 256);
}

// Add two 2048 bit numbers
// a + b = c
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
            basket.bytes[i] ^= basket.bytes[i-1] & 0x80 && i ? 0x01 : 0x00;

            b.bytes[i] = basket.bytes[i];

            j = b.bytes[i] ? 1 : 0;
        }
    }

    return a;
}

uint2048_t subtract2048(uint2048_t a, uint2048_t b) {
    uint2048_t basket;
    init2048(&basket);

    int j = 1;
    
    while(j) {

        j = 0;

        for(int i = 0; i < 256; ++i) {
            basket.bytes[i] = (~a.bytes[i]) & b.bytes[i];
            a.bytes[i] ^= b.bytes[i];
            j = basket.bytes[i] ? 1 : 0;
        }

        for(int i = 255; i >= 0; --i) {
            basket.bytes[i] <<= 1;
            basket.bytes[i] = basket.bytes[i - 1] & 0x80 && i ? 0x1 : 0x0;
        }

        b = basket;
    }
    return a;
}

// Multiply two 2048 bit numbers
// Outputs a 4096 bit number
// a * b = c
uint4096_t multiply2048(uint2048_t a, uint2048_t b) {
    uint4096_t c;
    init4096(&c);

    uint4096_t out;
    init4096(&out);

    for(int i = 0; i < 256; ++i) {
        c.bytes[i] = a.bytes[i];
    }

    for(int i = 0; i < 256; ++i) {
        for(int j = 0; j < 8; ++j) {
            
            out = b.bytes[i] & 0x1 ? add4096(out, c) : out;

            for(int k = 511; k >= 0; --k) {
                c.bytes[k] <<= 1;
                c.bytes[k] ^= c.bytes[k - 1] & 0x80 && k ? 0x1 : 0x0;
            }

            b.bytes[i] >>= 1;
        }
    }

    return out;
}

//###########################################################


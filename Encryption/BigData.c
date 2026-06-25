#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    uint64_t chunks[8];
} uint512_t;

void init512(uint512_t *num) {
    memset(num->chunks, 0, sizeof(num->chunks));
}

void add512(uint512_t *a, uint512_t *b) {
    uint512_t buffer0;
    uint8_t buffer1 = 0;
    uint64_t bases[] = {0x01ULL,0x8000000000000000ULL};
    init512(&buffer0);
    while(b->chunks[0]||b->chunks[1]||b->chunks[2]||b->chunks[3]||b->chunks[4]||b->chunks[5]||b->chunks[6]||b->chunks[7]) {
        for(int i = 0; i < 8; ++i) {
            buffer0.chunks[i] = a->chunks[i]&b->chunks[i];
            buffer1 <<= 1;
            if(buffer0.chunks[i]&bases[1]) {
                buffer1 ^= 1;
            }
            buffer0.chunks[i] <<= 1;
        }
        buffer1 >>= 1;
        for(int i = 7; i >= 0; --i) {
            if(buffer1&0x01) {
                buffer0.chunks[i] ^= bases[0];
            }
            buffer1 >>= 1;
        }
        for(int i = 0; i < 8; ++i) {
            a->chunks[i] ^= b->chunks[i];
            b->chunks[i] = buffer0.chunks[i];
        }
    }
    
}

int main() {
    uint512_t a;
    uint512_t b;
    init512(&a);
    init512(&b);
    uint64_t a1 = 0xFFFFFFFFFFFFFFFFULL;
    uint64_t b1 = 2ULL;
    a.chunks[0] = a1;
    b.chunks[0] = b1;
    add512(&a,&b);
    for(int i = 7; i >= 0; --i) {
        for(int j = 0; j < 64; ++j) {
            if(a.chunks[i]&0x8000000000000000ULL) {
                printf("%u",1);
            } else {
                printf("%u",0);
            }
            a.chunks[i] <<= 1;
        }
    }
    printf("\n");
    return 0;
}
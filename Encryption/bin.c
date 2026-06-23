#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int* bin(int unsigned n) {
    int *out = (int*)calloc(32, sizeof(int));
    if(n == 0) {
        return out;
    } else {
        for(int i = 0; i < 32; ++i) {
            out[i] = (int)pow(2,i) * (n & 1);
            n >>= 1;
            if(n == 0) {
                i = 32;
            }
        }
    }
    return out;
}

int main() {
    int unsigned value = 1134;
    int* binary = bin(value);
    for(int i = 0; i < 32; ++i) {
        printf("%d\n", binary[i]);
    }
    return 0;
}
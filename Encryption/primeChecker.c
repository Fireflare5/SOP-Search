#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// IsPrime uses the Miller-Rabin Primality Test.
// n-1 = d(2^s).
// 2 ≤ a ≤ n-2.
// If a^d % n = 1.
// Or a^(d2^r) % n = n-1 (Possible Prime).
// Repeat while false for all values 0 ≤ r < s.
// If false then n is not prime.
// If true try a different value of a.
// Multiple Trues indicate n is likely prime.
int IsPrime(int n) {
    if(n % 2 != 1 || n < 2) {
        return 0;
    } else if(n == 2) {
        return 1;
    } else {
        int *rads = calloc(4, sizeof(int)); // Order r, a, d, s
        while(rads[2] * pow(2, rads[3]) != n-1) {
            rads[2] = 1;
            rads[3]++;
            while(rads[2] * pow(2, rads[3]) < n-1) {
                rads[2] += 2;
            }
        }
        printf("%d %d\n", rads[2], rads[3]);
        return 0;
    }
}

int main() {
    int x = IsPrime(67289);
    return 0;
}
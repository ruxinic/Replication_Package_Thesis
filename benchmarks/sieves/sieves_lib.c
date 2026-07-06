#include <stdlib.h>
#include <stdint.h>
#include <string.h>

// compute sieves and returns the total number of primes found
// populates an output array with the prime values up to the limit
int compute_sieve(int limit, int* out_primes) {
    if (limit < 2) return 0;

    // allocate 1 byte per number. Consumes only ~100MB for limit=100,000,000
    uint8_t* is_prime = (uint8_t*)malloc((limit + 1) * sizeof(uint8_t));
    if (is_prime == NULL) return 0;

    // initialize all values to 1 (True)
    memset(is_prime, 1, limit + 1);
    is_prime[0] = 0;
    is_prime[1] = 0;

    // run the Sieves elimination loop
    for (int n = 2; n * n <= limit; n++) {
        if (is_prime[n]) {
            // elimination stride runs instantly in pure hardware memory lines
            for (int i = n * n; i <= limit; i += n) {
                is_prime[i] = 0;
            }
        }
    }

    // collect the prime values into pre-allocated output buffer
    int count = 0;
    for (int i = 2; i <= limit; i++) {
        if (is_prime[i]) {
            out_primes[count] = i;
            count++;
        }
    }

    free(is_prime);
    return count;
}
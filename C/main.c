#include <stdio.h>
#include <math.h>
#include <time.h>
#include <stdlib.h>


void calculate_primes(int n, int *count, double *time_taken) {
    int sqrt_n = (int)sqrt(n);
    int *prime_list = malloc(sqrt_n * sizeof(int)); // Initial memory allocation
    int p_count = 0;

    clock_t t1, t2;
    t1 = clock();

    for (int i = 2; i <= n; i++) {
        int prime = 1; // Initialize prime as 1 for each iteration
        for (int j = 0; j < p_count; j++) {
            if (i % prime_list[j] == 0) {
                prime = 0;
                break;
            }
        }
        if (prime == 1) {
            *count = *count + 1;
            if (p_count <= sqrt_n) {
                // Reallocate more memory in chunks
                prime_list[p_count] = i;
                p_count++;
            }
        }
    }
    t2 = clock();
    *time_taken = ((double)(t2 - t1)) / CLOCKS_PER_SEC;

    free(prime_list);
}


void try_10() {
    for (int i = 0; i < 15; i++) {
        int n = pow(10, i);
        int count = 0;
        double time_taken;
        calculate_primes(n, &count, &time_taken);
        printf("%d %d %f\n", i, count, time_taken);
    }
}

int main() {
    try_10();
    return 0;
}

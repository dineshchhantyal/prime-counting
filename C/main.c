#include <stdio.h>
#include <math.h>
#include <time.h>
#include <stdlib.h> // Include the stdlib.h header for malloc and free

void calculate_primes(int n, int *count, double *time_taken) {
    int sqrt_n = (int)sqrt(n);
    int *prime_list = malloc(sqrt_n * sizeof(int)); // Dynamically allocate memory
    int p_count = 0;
    *count = 0;

    clock_t t1, t2;
    t1 = clock();
    for (int i = 2; i <= n; i++) {
        int prime = 1;
        for (int j = 0; j < p_count; j++) {
            if (i % prime_list[j] == 0) {
                prime = 0;
                break;
            }
        }
        if (prime) {
            (*count)++;
            if (i <= sqrt_n) {
                p_count++;
                prime_list[*count - 1] = i;
            }
        }
    }
    t2 = clock();
    *time_taken = ((double)(t2 - t1)) / CLOCKS_PER_SEC;

    // Free dynamically allocated memory
    free(prime_list);
}

void try_10() {
    for (int i = 0; i < 20; i++) {
        int n = pow(10, i);
        int count;
        double time_taken;
        calculate_primes(n, &count, &time_taken);
        printf("%d %d %f\n", i, count, time_taken);
    }
}

int main() {
    try_10();
    return 0;
}

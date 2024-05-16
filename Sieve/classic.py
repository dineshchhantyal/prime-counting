import time
import numpy as np
import sys


def sieve_classic(n):
    t1 = time.perf_counter()  # Start timing

    if n < 2:
        return 0, time.perf_counter() - t1

    # is_prime = [True] * (n+1)
    is_prime = np.ones(n+1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    count = 0

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False

    count = sum(is_prime)  # Directly count the primes

    t2 = time.perf_counter()  # End timing
    return count, t2 - t1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            n = int(sys.argv[i])
            ans, time_taken = sieve_classic(n)
            print(f"{n}: ans = {ans} and time taken = {round(time_taken, 4)}")
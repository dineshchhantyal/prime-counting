

import time

def calculate_root_n_prime(n):
    is_prime = [True] * (n+1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False

    return is_prime

def sieve(n):
    if n < 2:
        return 0, 0

    t1 = time.perf_counter()  # Start timing

    root_n = int(n**0.5) + 1
    root_primes = calculate_root_n_prime(root_n)

    size = 10**5
    count = 0
    for k in range(root_n + 1, n, size):
        is_prime = [True] * (min(n+1, k+size) - k)
        segment_start = k
        for i in range(2, root_n):
            if root_primes[i]:
                # Find the start value in the current segment for marking multiples
                start = max(i*i, (segment_start + i - 1) // i * i)
                for j in range(start, k+size, i):
                    if j > n:
                        break
                    is_prime[j - segment_start] = False
        count += sum(is_prime)

    count += sum(root_primes[2:])  # Directly count the primes, excluding 0 and 1

    t2 = time.perf_counter()  # End timing
    return count, t2 - t1


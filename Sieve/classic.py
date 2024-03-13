import time


def sieve(n):
    t1 = time.perf_counter()  # Start timing

    if n < 2:
        return 0, time.perf_counter() - t1

    is_prime = [True] * (n+1)
    is_prime[0] = is_prime[1] = False
    count = 0

    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False

    count = sum(is_prime)  # Directly count the primes

    t2 = time.perf_counter()  # End timing
    return count, t2 - t1

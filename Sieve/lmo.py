import time
import numpy as np
import math
from functools import lru_cache


def phi(x, a, primes):
    """
    Legendre's phi function φ(x,a) - counts numbers <= x not divisible by any of the
    first a primes. Key component of LMO algorithm.
    """
    if a == 0:
        return x
    if x <= 0:
        return 0
    if a <= 0:
        return x

    if a == 1:
        # Special case for a=1 (excluding multiples of 2)
        return (x + 1) // 2

    # Recursive implementation of phi using inclusion-exclusion principle
    if x <= primes[a - 1]:
        return 1

    result = phi(x, a - 1, primes)
    result -= phi(x // primes[a - 1], a - 1, primes)
    return result


@lru_cache(maxsize=10**6)
def pi_small(x):
    """Count primes <= x for small values using simple sieve."""
    if x < 2:
        return 0

    sieve = np.ones(x + 1, dtype=bool)
    sieve[0:2] = False

    for i in range(2, int(math.sqrt(x)) + 1):
        if sieve[i]:
            sieve[i * i :: i] = False

    return np.sum(sieve)


def P2(x, a, primes):
    """
    Calculates P₂(x,a) sum component of the LMO algorithm.
    This computes the contribution of numbers with exactly 2 prime factors.
    """
    result = 0

    # Loop through primes p_i where i <= a
    for i in range(a):
        p = primes[i]
        if p * p > x:
            break

        # Add contribution of numbers divisible by p_i and another prime > p_i
        result += pi_small(x // p) - pi_small(p)

        # Subtract contribution of numbers divisible by p_i and p_j where j < i
        for j in range(i):
            q = primes[j]
            if p * q > x:
                break
            result -= 1

    return result


def lmo_prime_count(n):
    """
    Lagarias-Miller-Odlyzko algorithm for counting primes <= n.
    Optimized for very large values of n.
    """
    if n < 2:
        return 0, 0

    t1 = time.perf_counter()

    # For small numbers, use simpler methods
    if n <= 10**9:
        return pi_small(n), time.perf_counter() - t1

    # Step 1: Determine a suitable value for a (parameter for phi function)
    # Theoretical optimal is around n^(1/3), but needs tuning for specific ranges
    a = int(
        n ** (1 / 3.5)
    )  # Slightly smaller than theoretical for practical performance

    # Step 2: Calculate all primes up to n^(1/2+ε)
    sqrt_n = int(math.sqrt(n)) + 1

    # Generate primes up to sqrt(n)
    is_prime = np.ones(sqrt_n + 1, dtype=bool)
    is_prime[0:2] = False

    for i in range(2, int(math.sqrt(sqrt_n)) + 1):
        if is_prime[i]:
            is_prime[i * i :: i] = False

    primes = np.where(is_prime)[0]

    # Step 3: Use Legendre's formula with LMO optimizations
    result = phi(n, a, primes) + a - 1 - P2(n, a, primes)

    t2 = time.perf_counter()
    return result, t2 - t1


def main():
    for n in range(1, 13):  # Testing up to 10^12
        num = 10**n
        count, time_taken = lmo_prime_count(num)
        print(f"Primes <= 10^{n}: {count}")
        print(f"Time: {time_taken:.6f} seconds")
        print()


if __name__ == "__main__":
    main()

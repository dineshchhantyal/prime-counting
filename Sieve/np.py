import time
import numpy as np
from multiprocessing import Pool, cpu_count
import math

# Precompute a wheel pattern for numbers not divisible by 2,3,5
wheel_increments = [4, 2, 4, 2, 4, 6, 2, 6]

# Process in blocks of 2^16 to optimize cache usage
BLOCK_SIZE = 2**16


def sieve(n):
    if n < 2:
        return 0, 0

    t1 = time.perf_counter()

    # Simple approach for small n
    if n <= 10**8:
        # Create a boolean array for all numbers up to n
        is_prime = np.ones(n + 1, dtype=bool)
        is_prime[0:2] = False  # 0 and 1 are not prime

        # Sieve of Eratosthenes
        for i in range(2, int(math.sqrt(n)) + 1):
            if is_prime[i]:
                is_prime[i * i :: i] = False

        # 1 bit per number instead of 8 bits (bool)
        is_prime_bits = np.packbits(is_prime)

        count = np.sum(is_prime)
        t2 = time.perf_counter()
        return count, t2 - t1

    # For larger numbers, use segmented sieve
    sqrt_n = int(math.sqrt(n)) + 1

    # Get primes up to sqrt(n)
    small_primes = np.ones(sqrt_n + 1, dtype=bool)
    small_primes[0:2] = False

    for i in range(2, int(math.sqrt(sqrt_n)) + 1):
        if small_primes[i]:
            small_primes[i * i :: i] = False

    primes = np.nonzero(small_primes)[0]
    count = len(primes)  # Count of primes <= sqrt(n)

    # Process segments
    segment_size = min(10**8, n // cpu_count())

    # Create segments
    segments = []
    for segment_start in range(sqrt_n + 1, n + 1, segment_size):
        segment_end = min(n + 1, segment_start + segment_size)
        segments.append((segment_start, segment_end, primes))

    # Process segments in parallel
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(process_segment_corrected, segments)
        count += sum(results)

    t2 = time.perf_counter()
    return count, t2 - t1


def process_segment_corrected(args):
    segment_start, segment_end, primes = args
    segment_size = segment_end - segment_start

    # Initialize segment: all numbers in range are potential primes
    segment = np.ones(segment_size, dtype=bool)

    # Sieve with each prime
    for p in primes:
        # Find first multiple of p in segment
        start_idx = (-(segment_start % p)) % p
        if start_idx < segment_size:
            segment[start_idx::p] = False

    return np.sum(segment)


def sieve_bit_packed(n):
    """Memory-efficient prime counting"""
    if n < 2:
        return 0, 0

    t1 = time.perf_counter()

    if n == 2:
        return 1, time.perf_counter() - t1

    # Count 2 separately
    count = 1

    # Only track odd numbers
    is_prime = np.ones((n - 1) // 2 + 1, dtype=bool)
    is_prime[0] = False  # 1 is not prime

    limit = int(math.sqrt(n))

    # Only need to check odd numbers up to sqrt(n)
    for i in range(1, (limit - 1) // 2 + 1):
        if is_prime[i]:
            p = 2 * i + 1
            # Mark odd multiples
            start = (p * p - 1) // 2
            is_prime[start::p] = False

    count += np.sum(is_prime)

    t2 = time.perf_counter()
    return count, t2 - t1


def main():
    n = 11
    for n in range(20):
        num = 10**n
        count, time_taken = sieve(num)
        print(f"Count of primes below 10^{n}: {count}")
        print(f"Time taken: {time_taken:.6f} seconds")
        print()


if __name__ == "__main__":
    main()

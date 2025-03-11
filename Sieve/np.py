import time
import numpy as np

def calculate_root_n_prime(n):
    # Use boolean dtype for memory efficiency
    is_prime = np.ones(n + 1, dtype=np.bool_)
    is_prime[0:2] = False  # 0 and 1 are not primes

    # Optimization for even numbers
    is_prime[4::2] = False

    # Only odd numbers need checking after 2
    for i in range(3, int(n**0.5) + 1, 2):
        if is_prime[i]:
            # Vectorized operation - mark all multiples at once
            is_prime[i*i::i] = False

    return is_prime

def sieve(n):
    if n < 2:
        return 0, 0

    t1 = time.perf_counter()

    root_n = int(n**0.5) + 1
    root_primes = calculate_root_n_prime(root_n)

    # Get prime numbers up to sqrt(n) for sieving
    primes = np.nonzero(root_primes)[0]
    small_prime_count = len(primes)

    # Process in memory-efficient segments
    size = 10**6  # Larger chunks for better vectorization
    count = 0

    for segment_start in range(root_n + 1, n + 1, size):
        segment_end = min(n + 1, segment_start + size)
        segment_size = segment_end - segment_start

        # Initialize segment
        segment = np.ones(segment_size, dtype=np.bool_)

        # Handle even numbers in bulk
        if segment_start % 2 == 0:
            segment[0::2] = False
        else:
            segment[1::2] = False

        # Mark non-primes using vectorized operations
        for p in primes[1:]:  # Skip 2, already handled even numbers
            # Find first multiple of p in segment
            start = (-(segment_start % p)) % p
            if p * p > segment_start + start:
                start = p * p - segment_start
                if start >= segment_size:
                    continue

            # Mark all multiples at once
            segment[start::p] = False

        count += np.sum(segment)

    # Add primes below sqrt(n)
    count += np.sum(root_primes)

    t2 = time.perf_counter()
    return count, t2 - t1

def main():
    for i in range(21):  # 0 to 20
        n = 10**i
        count, time_taken = sieve(n)
        print(f"10^{i} = {n}:")
        print(f"Number of primes: {count}")
        print(f"Time taken: {time_taken:.4f} seconds")
        print("-" * 40)

if __name__ == '__main__':
    main()
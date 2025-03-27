import time
import numpy as np
from multiprocessing import Pool, cpu_count, shared_memory
from numba import njit
import math


# JIT-compile this critical function for speed
@njit
def mark_segment(segment, segment_start, primes):
    segment_size = len(segment)

    # Handle even numbers in bulk (2's multiples)
    if segment_start % 2 == 0:
        segment[0::2] = False
    else:
        segment[1::2] = False

    # Use wheel factorization - skip multiples of 2
    for p_idx in range(1, len(primes)):  # Skip 2
        p = primes[p_idx]

        # Find first multiple of p in segment
        start = (-(segment_start % p)) % p
        if p * p > segment_start + start:
            start = p * p - segment_start

        if start < segment_size:
            # Mark all multiples at once
            segment[start::p] = False

    return segment


def calculate_root_n_prime(n):
    limit = min(n, 10**8)  # Memory cap for larger numbers
    is_prime = np.ones(limit + 1, dtype=np.bool_)
    is_prime[0:2] = False

    # Only need to sieve up to sqrt(limit)
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            is_prime[i * i :: i] = False

    return is_prime, np.nonzero(is_prime)[0]


def process_segment(args):
    segment_start, segment_end, shared_name, primes_size, batch_id = args
    segment_size = segment_end - segment_start

    # Get primes from shared memory
    existing_shm = shared_memory.SharedMemory(name=shared_name)
    primes = np.ndarray((primes_size,), dtype=np.int64, buffer=existing_shm.buf)

    # Initialize segment
    segment = np.ones(segment_size, dtype=np.bool_)

    # Use JIT-compiled function for the heavy lifting
    segment = mark_segment(segment, segment_start, primes)

    # Clean up shared memory
    existing_shm.close()

    return np.sum(segment), batch_id


def sieve(n):
    if n < 2:
        return 0, 0

    t1 = time.perf_counter()

    # Calculate sqrt(n) primes more efficiently
    sqrt_n = int(math.sqrt(n)) + 1
    root_primes_array, primes = calculate_root_n_prime(sqrt_n)

    # Optimization: use shared memory for primes
    primes_size = len(primes)
    shm = shared_memory.SharedMemory(create=True, size=primes.nbytes)
    shared_primes = np.ndarray(primes.shape, dtype=primes.dtype, buffer=shm.buf)
    shared_primes[:] = primes[:]

    # Calculate optimal segment size
    num_cores = cpu_count()
    # Smaller segments for better cache locality
    size = max(10**5, min(10**7, n // (num_cores * 20)))

    # Create segments with batch IDs for tracking
    segments = []
    batch_id = 0
    for segment_start in range(sqrt_n + 1, n + 1, size):
        segment_end = min(n + 1, segment_start + size)
        segments.append((segment_start, segment_end, shm.name, primes_size, batch_id))
        batch_id += 1

    # Use imap_unordered for better load balancing
    count = 0
    with Pool(processes=num_cores) as pool:
        # Process results as they come in to avoid waiting for all
        for segment_count, _ in pool.imap_unordered(
            process_segment, segments, chunksize=1
        ):
            count += segment_count

    # Add primes below sqrt(n)
    count += np.sum(root_primes_array)

    # Clean up shared memory
    shm.close()
    shm.unlink()

    t2 = time.perf_counter()
    return count, t2 - t1


def main():
    n = 11

    num = 10**n
    count, time_taken = sieve(num)
    print(f"Count of primes below 10^{n}: {count}")
    print(f"Time taken: {time_taken:.6f} seconds")
    print()


if __name__ == "__main__":
    main()

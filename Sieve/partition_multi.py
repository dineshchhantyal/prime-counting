import time
from multiprocessing import Pool, cpu_count, freeze_support

def calculate_root_n_prime(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return is_prime

def process_segment(args):
    segment_start, segment_end, n, root_n, root_primes = args
    segment_size = segment_end - segment_start + 1
    is_prime = [True] * segment_size
    for i in range(2, root_n):
        if root_primes[i]:
            start = max(i * i, (segment_start + i - 1) // i * i)
            for j in range(start, segment_end + 1, i):
                is_prime[j - segment_start] = False
    return sum(is_prime)

def sieve(n):
    if n < 2:
        return 0, 0

    t1 = time.perf_counter()

    root_n = int(n**0.5) + 1
    root_primes = calculate_root_n_prime(root_n)

    num_processes = cpu_count()
    min_size = 10**5
    ideal_num_segments = 10 * num_processes
    size = max(min_size, (n - root_n) // ideal_num_segments)

    # Create segments
    segments = []
    k = root_n + 1
    while k <= n:
        segment_end = min(k + size - 1, n)
        segments.append((k, segment_end, n, root_n, root_primes))
        k = segment_end + 1

    # Process segments in parallel
    with Pool(processes=num_processes) as pool:
        results = pool.map(process_segment, segments)

    # Sum results and add root primes
    count = sum(results) + sum(root_primes[2:])

    t2 = time.perf_counter()
    return count, t2 - t1

def main():
    num = int(input("Enter the number: "))
    count, time_taken = sieve(num)
    print(f"Number of primes: {count}")
    print(f"Time taken: {time_taken:.4f} seconds")

if __name__ == '__main__':
    freeze_support()  # Required for Windows compatibility
    main()
import numpy as np
import pyopencl as cl
import time
from math import ceil

def sieve_gpu(n, chunk_size=100_000_000):
    # Initialize OpenCL
    platforms = cl.get_platforms()
    devices = platforms[0].get_devices(device_type=cl.device_type.GPU)
    context = cl.Context(devices)
    queue = cl.CommandQueue(context)

    t1 = time.perf_counter()
    total_count = 0

    # Process in chunks
    num_chunks = ceil(n / chunk_size)

    for chunk in range(num_chunks):
        start = chunk * chunk_size
        end = min((chunk + 1) * chunk_size, n)
        size = end - start + 1

        # Create boolean array for this chunk
        is_prime = np.ones(size, dtype=np.int32)

        # Transfer chunk data to GPU
        mf = cl.mem_flags
        is_prime_gpu = cl.Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=is_prime)

        # OpenCL kernel for chunk processing
        kernel_code = """
        __kernel void mark_multiples(__global int* is_prime,
                                   const int chunk_start,
                                   const int chunk_size,
                                   const int prime) {
            int gid = get_global_id(0);
            int start = max(prime * prime,
                          ((chunk_start + prime - 1) / prime) * prime) + gid * prime;
            start = start - chunk_start;

            for(int i = start; i < chunk_size; i += prime) {
                is_prime[i] = 0;
            }
        }
        """

        program = cl.Program(context, kernel_code).build()

        # Mark non-primes in chunk
        sqrt_n = int(np.sqrt(end)) + 1
        for i in range(2, sqrt_n):
            if start <= i * i <= end:  # Only process relevant primes
                global_size = (max(1, (size - i * i) // i + 1),)
                program.mark_multiples(queue, global_size, None,
                                     is_prime_gpu,
                                     np.int32(start),
                                     np.int32(size),
                                     np.int32(i))

        # Get results back from GPU
        cl.enqueue_copy(queue, is_prime, is_prime_gpu)
        chunk_count = np.sum(is_prime)
        total_count += chunk_count

    t2 = time.perf_counter()
    return total_count, t2 - t1

def main():
    try:
        num = int(input("Enter the number: "))
        if num < 0:
            raise ValueError("Number must be positive")
        count, time_taken = sieve_gpu(num)
        print(f"Number of primes: {count}")
        print(f"Time taken: {time_taken:.4f} seconds")
    except ValueError as e:
        print(f"Error: {e}")
    except cl.LogicError as e:
        print(f"OpenCL error: {e}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")

if __name__ == '__main__':
    main()
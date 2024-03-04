import asyncio
import time

# Define an efficient accumulator function


async def accumulate_sum(start, end):
    """
    Calculates the sum of integers in a given range efficiently
    using the iterative approach.

    Args:
        start: The starting integer of the range (inclusive).
        end: The ending integer of the range (inclusive).

    Returns:
        The calculated sum.
    """
    total = 0
    for i in range(start, end + 1):
        total += i
    return total


async def main():
    # Use the accumulator function for both calculations
    n1, n2 = 10**4, 10**8  # Improved variable naming for clarity
    t0 = time.perf_counter()
    sum1 = await accumulate_sum(1, n1)
    t1 = time.perf_counter()

    sum2 = await accumulate_sum(10**4, n2)
    t2 = time.perf_counter()

    total_sum = sum1 + sum2  # Calculate the total sum efficiently
    print("Sum:", total_sum)
    print("Time taken for first calculation:", t1 - t0)
    print("Time taken for second calculation:", t2 - t1)
    print("Total time taken:", t2 - t0)

asyncio.run(main())

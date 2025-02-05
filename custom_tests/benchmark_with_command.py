"""
This module is used to test the benchmark_with_command function in the
benchmark module.
"""

from LessThanSqrt.main import lts
from PrimeLessThanSqrt.main import prime_lts
from Sieve.classic import sieve_classic
from Sieve.partition import sieve as sieve_partitioned

from sympy import primepi


methods = [lts, prime_lts, sieve_classic, sieve_partitioned]


async def benchmark_with_command(num):
    """
    This function is used to benchmark the performance of the functions in the
    methods list.
    """
    for method in methods:
        ct, time_taken = method(num)

        print(
            f"""Method: {method.__name__}, count: {ct}, \
                correct: {primepi(num)}, time taken: {time_taken} """
        )

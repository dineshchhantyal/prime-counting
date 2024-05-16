"""
Check the performance of all the algorithms in the custom dataset.
"""

from LessThanSqrt.main import lts
from PrimeLessThanSqrt.main import prime_lts
from Sieve.classic import sieve_classic
from Sieve.partition import sieve as sieve_partitioned
from .check_custom_data_set_by_method import test as check


methods = [lts, prime_lts, sieve_classic, sieve_partitioned]


async def benchmark_custom_dataset():
    for method in methods:
        total_time, corret_ct, incorrect_ct = await check(method)

        print(f"Method: {method.__name__}")
        print(f"Total time taken: {round(total_time, 4)}")
        print("Results:")
        print(f"Total tests: {corret_ct + incorrect_ct}")
        print(f"Correct: {corret_ct}")
        print(f"Incorrect: {incorrect_ct}")
        print("\n")

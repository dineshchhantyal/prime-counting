from LessThanSqrt.main import lts
from PrimeLessThanSqrt.main import prime_lts
from Sieve.classic import sieve_classic
from Sieve.partition import sieve as sieve_partitioned
from tests.check_custom_data_set_by_method import test as check

import asyncio


def guide():
    # print user to select the method
    print(
        "Select the method to calculate the number of prime numbers less than a given number:"
    )
    print("1. Less than the square root method")
    print("2. Prime less than the square root method")
    print("3. Sieve of Eratosthenes method")
    print("4. Sieve of Eratosthenes method (partitioned)")
    method = int(input("Enter the number of the method: "))

    method_func = None

    if method == 1:
        method_func = lts
    elif method == 2:
        method_func = prime_lts
    elif method == 3:
        method_func = sieve_classic
    elif method == 4:
        method_func = sieve_partitioned
    else:
        print("Invalid method selected")
        exit()

    return method_func


async def print_results(total_time, corret_ct, incorrect_ct):
    print(f"Total time taken: {round(total_time, 4)}")
    print("Results:")
    print(f"Total tests: {corret_ct + incorrect_ct}")
    print(f"Correct: {corret_ct}")
    print(f"Incorrect: {incorrect_ct}")
    print("\n")


def test_with_command():
    method_func = guide()
    total_time, corret_ct, incorrect_ct = asyncio.run(check(method_func))
    asyncio.run(print_results(total_time, corret_ct, incorrect_ct))
    print("All tests completed")

from sympy import primepi
import os
import time

from LessThanSqrt.main import lts
from PrimeLessThanSqrt.main import prime_lts
from Sieve.classic import sieve_classic
from Sieve.partition import sieve as sieve_partitioned

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

correct_ct = 0
incorrect_ct = 0

t1 = time.time()
with open(os.getcwd() + "/test.txt", "r") as f:
    for line in f:
        num = int(line.strip())
        ans = primepi(num)
        main_ans, time_taken = method_func(num)
        if ans == main_ans:
            correct_ct += 1
            print(
                f"""
✔︎ {num}: ans = {ans} and time taken = {round(time_taken, 4)}
"""
            )
        else:
            incorrect_ct += 1
            print(f"✘ {num}: expected = {ans} and got = {main_ans}")

t2 = time.time()
print("All tests completed")

print(f"Total time taken: {round(t2 - t1, 4)}")
print("Results:")
print(f"Total tests: {correct_ct + incorrect_ct}")
print(f"Correct: {correct_ct}")
print(f"Incorrect: {incorrect_ct}")

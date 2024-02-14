import math
import time
import numpy as np

def prime_numbers(num):
    ct = 0
    for i in range(2, num + 1):
        is_prime = True
        if i % 2 == 0:
            is_prime= False
        for j in range(2,math.floor(math.sqrt(i)) + 1):
            if i % j == 0:
                is_prime= False
        if is_prime:
            ct += 1
    return ct

# start timer
time1 = time.time()

# print(prime_numbers(1000000))  # [2, 3, 5, 7]

print(prime_numbers(10**8))  # [2, 3, 5, 7]

# end timer
time2 = time.time()

print('Time taken: ', time2 - time1, 'seconds')

# primes = np.arange(2, 100000000)

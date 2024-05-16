import math
import time


def lts(num):
    time1 = time.time()

    ct = 1 if num >= 2 else 0
    for i in range(3, num + 1):
        is_prime = True
        if i % 2 == 0:
            is_prime = False
        for j in range(2, math.floor(math.sqrt(i)) + 1):
            if i % j == 0:
                is_prime = False
        if is_prime:
            ct += 1
    time2 = time.time()

    return ct, time2 - time1

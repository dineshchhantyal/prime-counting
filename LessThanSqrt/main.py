import math
import time
import numpy as np

def lts(num):
    time1 = time.time()

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
    time2 = time.time()

    return ct, time2 - time1


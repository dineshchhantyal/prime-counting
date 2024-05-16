import time

import sympy as sp


def prime_lts(n):
    sqrt_n = int(n**0.5)
    prime_list = list(sp.primerange(0, sqrt_n + 1))
    ct = len(prime_list)

    t1 = time.time()
    for i in range(sqrt_n + 1, n + 1):
        ct += 1
        for prime in prime_list:
            if i % prime == 0:
                ct -= 1
                break

    t2 = time.time()
    return ct, t2 - t1


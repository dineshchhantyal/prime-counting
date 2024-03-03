# - [ ] - make a list 2 - n
# - [ ] - loop from 2 - n remove every multiple of n from the list
# - [ ] - return the list
import time


def main(n):
    t1 = time.time()
    primes = list(range(2, n+1))
    for i in primes:
        for j in range(i*2, n+1, i):
            if j <= n:
                try:
                    primes.remove(j)
                except ValueError:
                    pass
    t2 = time.time()
    return len(primes), t2 - t1

import math
import time

def erathosthenes_sieve(n):
    numbers = []
    
    for i in range(2,n):
        numbers.append(1)
        
    for i in range(2,(int(math.sqrt(n)))+1):
        
            for j in range(i*i,n, i):
                numbers[j-2] = 0
    return n-numbers.count(0)-2

t1 = time.time()
primes = erathosthenes_sieve(10**3)
t2 = time.time()

print("No. of primes:",primes)
print("time", (t2-t1))

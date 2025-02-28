from erathosthenes_sieve import erathosthenes_sieve
import time

test_val = 10000000

t1= time.time()
total_prime = erathosthenes_sieve(test_val)
t2 = time.time()

print("Total count of prime numbers below",test_val,"is",total_prime)
print("time taken:",(t2-t1))
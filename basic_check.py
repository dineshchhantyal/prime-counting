from is_prime import check_prime
import time
def basic_check(val):
    total = 0
    for i in range(val):
        if check_prime(i):
            total += 1
    return total

test_val = 1000

t1= time.time()
total_prime =basic_check(test_val)
t2= time.time() 

print("Total count of prime numbers below",test_val,"is",total_prime)
print("time taken:",(t2-t1))


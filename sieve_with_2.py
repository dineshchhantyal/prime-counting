import math
import time

def erathosthenes_sieve(n):
    numbers = []
    
    for i in range(3,n+1,2):
        numbers.append(1)
    
        
    for i in range(3,(int(math.sqrt(n)))+1,2):
           
        for j in range(i*i,n+1, 2*i):
            
            numbers[int((j-3)/2)] = 0
    #
    return numbers.count(1)+1

val = 10**4

print(erathosthenes_sieve(val))


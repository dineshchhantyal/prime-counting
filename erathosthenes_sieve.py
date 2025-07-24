import math
'''
This functions uses erathosthenes sieve method to determine the number of prime below n.
At first, all the numbers from 2 to n are stored in a list.
Then starting from 2 to (square root of n + 1) it replaces their multiples with zero.
All the remaining non-zero numbers are prime numbers.

'''


def erathosthenes_sieve(n):
    numbers = []
    
    for i in range(2,n):
        numbers.append(i)
        
    for i in range(2,(int(math.sqrt(n)))+1):
        
            for j in range(i*i,n, i):
                numbers[j-2] = 0
    return n-numbers.count(0)-2
    # return numbers    

print(erathosthenes_sieve(10**4))

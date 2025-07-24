import math
import time

def erathosthenes_sieve(n):
    numbers = []
    
    for i in range(2,n+1):
        numbers.append(i)
        
    for i in range(2,(int(math.sqrt(n)))+1):
        
            for j in range(i*i,n, i):
                numbers[j-2] = 0
    
    return [x for x in numbers if x != 0]

# print(erathosthenes_sieve(100))
# def phi_func(x,a,prime_num):
#     if n == 1:
#         return 1
#     result = n
#     prime_num = erathosthenes_sieve(n)
#     for num in prime_num:a
#         if num*num > n:
#             break
#         if n%num==0:
#             while n%num == 0:
#                 n = n//num
#                 result = result - result//num
#     if n > 1:
#         result = result - result//n
        
#     return result

# def pi(x):
#     if x < 2:
#         return 0
    
#     y = int(x ** (1/3))
#     primes = erathosthenes_sieve(y)
#     a = len(primes)
    
#     pi_x = phi_func(x, a, )

# print(pi(10000000))

# def prime_factors(n):
#     factors = []
    
#     # Check for the number of 2s that divide n
#     while n % 2 == 0:
#         factors.append(2)
#         n //= 2
    
#     # Check for odd factors from 3 onwards
#     for i in range(3, int(n**0.5) + 1, 2):
#         while n % i == 0:
#             factors.append(i)
#             n //= i
    
#     # If n is a prime number greater than 2
#     if n > 2:
#         factors.append(n)
    
#     return set(factors)

# print(prime_factors(100000))

# def phi_func(x,a, prime_list):
#     if a < 2:
#         return prime_list
#     result = None
#     for num in range(x+1):
#         factors = prime_factors(num)
#         for i in factors:
#             if i >= prime_list[a]:
#                result = prime_list.index(i)
#                break
#     return prime_list[result:]

# print(phi_func(100,2,erathosthenes_sieve(100)))

def phi_func(x,a, prime_list):
    new_prime_list = prime_list[:a]
    new_list = []
    for i in range(2, x+1):
        isPrime = True
        for j in new_prime_list:
            if (i % j == 0):
                isPrime = False
                break
        if isPrime:
            new_list.append(i)
    return new_list

def p2_func(x,a,prime_list):
    new_prime_list = prime_list[a:]
    count = 0
    for i in range(len(new_prime_list)):
        for j in range(i,len(new_prime_list)):
            if new_prime_list[i] * new_prime_list[j] <= x:
                count += 1
            else:
                break
                
    return count

def pi(x):
    primes = erathosthenes_sieve(int(math.sqrt(x)))
    a = len(primes)
    new_list = phi_func(x,a,primes)
    p2 = p2_func(x,a,primes)
    phi = len(new_list)
    
    return phi + a - 1 - p2

val = 10**9
t1= time.time()
print(f"pi({val}) is :",pi(val))
t2= time.time()
print("time taken in seconds is",(t2-t1))

                

                
            
    
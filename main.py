import time


def main(n):
    sqrt_n = int(n**0.5)
    prime_list = []
    ct = 0

    t1 = time.time()
    for i in range(2, n + 1):
        prime = 1
        for prime in prime_list:
            if i % prime == 0:
                prime = 0
                break
        if prime:
            ct += 1
            if i <= sqrt_n:
                prime_list.append(i)
    t2 = time.time()
    return ct, t2 - t1


def try_10():
    for i in range(20):
        count, time_taken = main(10**i)
        print(i, count, time_taken)


try_10()



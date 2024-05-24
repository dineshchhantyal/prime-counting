from PrimeCount import PrimeCount
import time
import sys

if __name__ == "__main__":
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    pc = PrimeCount(num)
    start = time.time()
    pc.count()
    end = time.time()
    print(f"Time taken: {end-start} seconds")
    print("The number of primes less than or equal to", num, "is", pc.count())

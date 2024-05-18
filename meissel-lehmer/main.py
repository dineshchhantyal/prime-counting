from PrimeCount import PrimeCount
from matplotlib import pyplot as plt
import time

if __name__ == "__main__":
    xs = [i for i in range(1, 50)]
    # p2s = [PrimeCount(i).count() for i in xs]
    # times = [i * 0.0001 for i in xs]

    p2s = []
    time_taken = []
    for i in xs:
        t1 = time.time()
        pc = PrimeCount(i)
        p2s.append(pc.count())
        t2 = time.time()
        time_taken.append(t2 - t1)
    plt.plot(xs, p2s)
    plt.xlabel("x")
    plt.ylabel("P2(x)")
    plt.title("P2(x) vs x")
    plt.show()

    plt.plot(xs, time_taken)
    plt.xlabel("x")
    plt.ylabel("Time taken")
    plt.title("Time taken vs x")
    plt.show()

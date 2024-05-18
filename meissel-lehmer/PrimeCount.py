""""
This module is used to count the number of
prime numbers less than or equal to
x using the Meissel-Lehmer algorithm.
"""

from P import P


class PrimeCount:
    def __init__(self, num):
        self.num = num

    def count(self):
        """
        This function is used to count the number of
        prime numbers less than or equal to x.
        """

        # evaluate P2(x)
        p = P(self.num)
        p2 = p._p2()

        print("P2(x) calculated")
        print(f"P2({self.num}): {p2}")

        return p2

""""
This module is used to count the number of
prime numbers less than or equal to
x using the Meissel-Lehmer algorithm.
"""

from P import P
from S import S


class PrimeCount:
    def __init__(self, num):
        self.x = num
        self.y = num ** (1 / 3)

    def count(self):
        """
        This function is used to count the number of
        prime numbers less than or equal to x.
        """

        # evaluate P2(x)
        p = P(self.x, self.y)
        p2 = p._p2()

        phi = self._phi()

        print(f"P2({self.x}): {p2}")

        print(f"phi({self.x}): {phi}")

        return p2

    def _phi(self):
        s = S(self.x, self.y)

        return s._S0() + s._S()

"""
This module is used to computed the value for original and special leaves
"""

from sympy.ntheory import mobius as mu
from sympy import primepi as pi


class S:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def _S0(self):
        """
        This function is used to compute the value of original leaves
        """
        ans = 0
        i = 1
        while i <= self.y:
            ans += self.s0_calc(i)
            i += 1
        return ans

    def _S(self):
        """
        This function is used to compute the value of special leaves
        """
        return self._S1() + self._S2() + self._S3()

    def _S1(self):
        """
        This function is used to compute the value of special leaves
        """
        n = pi(self.y) - pi(self.y ** (1 / 3))
        return n * (n - 1) / 2

    def _S2(self):
        """
        This function is used to compute the value of special leaves
        """
        return self._U() + self._V()

    def _S3(self):
        """
        This function is used to compute the value of special leaves
        """
        return 0

    def _U(self):
        """
        This function is used to compute the value of U
        """
        p = (self.x / self.y) ** (1 / 2)
        a = pi(self.y)

        ans = 0

        while p <= self.y:
            ans += a - pi(self.x / (p * p))
        return ans

    def _V(self):
        """
        This function is used to compute the value of V
        """
        return 0

    def _V1(self):
        """
        This function is used to compute the value of V1
        """
        return 0

    def _V2(self):
        """
        This function is used to compute the value of V2
        """
        return 0

    def s0_calc(self, n):
        """
        This function is used to calculate S0(x, y)
        """
        return mu(n) * (self.x // (n))

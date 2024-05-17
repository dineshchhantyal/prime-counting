"""
This module is used to calculate P_k(x, a).

P_k(x, a) is counts of numbers less than equals to
x with exactly k prime factors, all larger than p_a.

p_a is the a-th prime number.
"""

from sympy import primepi as pi


class P:
    def __init__(self, x):
        self.x = x
        self.y = x ** (1 / 3)
        self.rot_x = x ** (1 / 2)

    def _pk(self, k):
        """
        This function is used to calculate P_k(x, a).
        """
        pass

    def _p2(self):
        """
        This function is used to calculate P2(x).
        """
        return self.p2_calc(self.x)

    def p2_calc(self, p):
        """
        This function is used to calculate P2(x).
        """

        if p <= self.rot_x:
            return self.p2_calc_1(p) + self.p2_calc(p + 1)
        else:
            return 0

    def p2_calc_1(self, p):
        """
        This function is used to calculate single unite of P2(x).
        """
        return pi(self.x / p) - pi(p) + 1

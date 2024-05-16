"""
This module is used to test the custom data set by method.
"""

import os
from sympy import primepi


async def test(method_func):
    total_time = 0
    corret_ct = 0
    incorrect_ct = 0

    with open(os.getcwd() + "/test.txt", "r") as f:
        for line in f:
            num = int(line.strip())
            ans = primepi(num)
            main_ans, time_taken = method_func(num)
            total_time += time_taken
            if ans == main_ans:
                corret_ct += 1
                print(
                    f"""
    ✔︎ {num}: ans = {ans} and time taken = {round(time_taken, 4)}
    """
                )
            else:
                incorrect_ct += 1
                print(f"✘ {num}: expected = {ans} and got = {main_ans}")

    return total_time, corret_ct, incorrect_ct

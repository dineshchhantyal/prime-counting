import os
from sympy import primepi
from Sieve.classic import sieve

with open(os.getcwd() + "/test.txt", "r") as f:
    for line in f:
        num = int(line.strip())
        ans = primepi(num)
        main_ans, time_taken = sieve(num)
        if ans == main_ans:
            print(f"""
✔︎ {num}: ans = {ans} and time taken = {round(time_taken, 4)}
""")
        else:
            print(f"✘ {num}: expected = {ans} and got = {main_ans}")
print("All tests passed! ✔︎")




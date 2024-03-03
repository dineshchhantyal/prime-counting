import os
from sympy import primepi
from Sieve.main import main

with open(os.getcwd() + "/test.txt", "r") as f:
    for line in f:
        num = int(line.strip())
        ans = primepi(num)
        main_ans, time_taken = main(num)
        if (ans == main_ans):
            print(f"""✔︎ {num}: ans = {ans} and time taken = \
                  {round(time_taken, 4)}""")
        else:
            print(f"""Test failed for {num} with ans {ans} and
                main_ans {main_ans} and time taken {time_taken}""")
print("All tests passed! ✔︎")




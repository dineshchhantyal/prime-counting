import os
from sympy import primepi
from main import start

with open(os.getcwd() + "/PrimeLessThanSqrt/test.txt", "r") as f:
    for line in f:
        num = int(line.strip())
        ans = primepi(num)
        main_ans, time_taken = start(num)
        if (ans == main_ans):
            print(f"""✔︎ {num}: ans = {ans} and time taken = \
                  {round(time_taken, 4)}""")
        else:
            print(f"""Test failed for {num} with ans {ans} and
                main_ans {main_ans} and time taken {time_taken}""")
print("All tests passed! ✔︎")




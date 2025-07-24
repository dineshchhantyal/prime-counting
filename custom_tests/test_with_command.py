import pandas as pd
import time
import math
import os
import psutil
from sympy import primepi
from concurrent.futures import ProcessPoolExecutor, as_completed
import traceback


async def check_single(method_func, n):
    start = time.time()
    main_ans, time_taken = method_func(n)
    ans = primepi(n)
    total_time = time.time() - start
    corret_ct = 1 if ans == main_ans else 0
    incorrect_ct = 0 if ans == main_ans else 1
    status = "OK" if ans == main_ans else "FAIL"
    pid = os.getpid()
    try:
        core_id = psutil.Process(pid).cpu_num()
    except Exception:
        core_id = -1
    return (
        {
            "algorithm": method_func.__name__,
            "n": n,
            "n_exp": int(round(math.log10(n))),
            "pi_n": int(ans),
            "result": int(main_ans),
            "status": status,
            "method_time": time_taken,
            "total_time": total_time,
            "pid": pid,
            "core_id": core_id,
        },
        total_time,
        corret_ct,
        incorrect_ct,
    )


import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from LessThanSqrt.main import lts
from PrimeLessThanSqrt.main import prime_lts
from Sieve.classic import sieve_classic
from Sieve.partition import sieve as sieve_partitioned
from custom_tests.check_custom_data_set_by_method import test as check
from meissel_lehmer.main import pi_deleglise_rivat
import asyncio


def guide(method):

    method_func = None

    if method == 1:
        method_func = lts
        print("1. Less than the square root method")
    elif method == 2:
        method_func = prime_lts
        print("2. Prime less than the square root method")
    elif method == 3:
        method_func = sieve_classic
        print("3. Sieve of Eratosthenes method")
    elif method == 4:
        method_func = sieve_partitioned
        print("4. Sieve of Eratosthenes method (partitioned)")
    elif method == 5:
        method_func = pi_deleglise_rivat
        print("5. Meissel-Lehmer method (Deleglise-Rivat)")
    else:
        print("Invalid method selected. Please try again.")
        return None

    return method_func


async def print_results(total_time, corret_ct, incorrect_ct):
    print(f"Total time taken: {round(total_time, 4)}")
    print("Results:")
    print(f"Total tests: {corret_ct + incorrect_ct}")
    print(f"Correct: {corret_ct}")
    print(f"Incorrect: {incorrect_ct}")
    print("\n")


def test_with_command():
    method_func = guide()
    total_time, corret_ct, incorrect_ct = asyncio.run(check(method_func))
    asyncio.run(print_results(total_time, corret_ct, incorrect_ct))
    print("All tests completed")


def run_single_n(args):
    method_func, n = args
    try:
        return asyncio.run(check_single(method_func, n))[0]  # Only return row
    except Exception as e:
        print(f"Exception for n={n}: {e}", flush=True)
        return {
            "algorithm": method_func.__name__,
            "n": n,
            "n_exp": int(round(math.log10(n))),
            "pi_n": -1,
            "result": -1,
            "status": "ERROR",
            "method_time": -1,
            "total_time": -1,
            "pid": os.getpid(),
            "core_id": -1,
        }


if __name__ == "__main__":
    # system args for method then call the guide function

    args = sys.argv[1:]
    if args:
        try:
            method = int(args[0])
            method_func = guide(method)
            if method_func:
                print(
                    f"{'n':>10} | {'pi(n)':>10} | {'result':>10} | {'status':>6} | {'method_time':>14} | {'total_time':>14} | {'pid':>8} | {'core':>6}"
                )
                print("-" * 100)
                results = []
                runPrallel = False

                if runPrallel:
                    import multiprocessing

                    num_workers = multiprocessing.cpu_count()
                    with ProcessPoolExecutor(max_workers=num_workers) as executor:
                        futures = [
                            executor.submit(run_single_n, (method_func, 10**i))
                            for i in range(1, 25)
                        ]
                        for future in as_completed(futures):
                            try:
                                row = future.result()
                                print(
                                    f"n = 10^{row['n_exp']:2d} | pi(n) = {row['pi_n']:8,d} | result = {row['result']:8,d} | status = {row['status']:4s} | method_time = {row['method_time']:10.4e} s | total_time = {row['total_time']:10.4e} s | pid = {row['pid']} | core = {row['core_id']}"
                                )
                                results.append(row)
                            except Exception as e:
                                print(f"Exception in worker: {e}", flush=True)
                                traceback.print_exc()
                else:
                    for i in range(1, 25):
                        row = run_single_n((method_func, 10**i))
                        print(
                            f"n = 10^{row['n_exp']:2d} | pi(n) = {row['pi_n']:8,d} | result = {row['result']:8,d} | status = {row['status']:4s} | method_time = {row['method_time']:10.4e} s | total_time = {row['total_time']:10.4e} s | pid = {row['pid']} | core = {row['core_id']}"
                        )
                        results.append(row)
                print("-" * 100)
                print("All tests completed")
                # Write results to CSV
                df = pd.DataFrame(results)
                algo_name = method_func.__name__
                df.to_csv(f"benchmark_{algo_name}.csv", index=False)
                print(f"Results written to benchmark_{algo_name}.csv")
        except ValueError:
            print("Invalid input. Please enter a number corresponding to the method.")
    else:
        print("No method selected. Please provide a method number as an argument.")

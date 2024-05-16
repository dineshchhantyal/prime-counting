from tests.test_with_command import test_with_command
from tests.benchmark_with_command import benchmark_with_command
from tests.benchmark_custom_dataset import benchmark_custom_dataset

import asyncio


def guide():
    print("1. Run the algorithm tests with the custom dataset")
    print("2. Run the benchmark with a command line")
    print("3. Run the benchmark with a custom dataset")


if __name__ == "__main__":
    guide()
    choice = input("Enter your choice: ")
    if choice == "1":
        test_with_command()
    elif choice == "2":
        num = int(input("Enter the number: "))
        asyncio.run(benchmark_with_command(num))
    elif choice == "3":
        asyncio.run(benchmark_custom_dataset())
    else:
        print("Invalid choice")

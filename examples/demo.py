from profiler.comparison import compare_functions


def func_a():
    total = 0
    for i in range(20_000_000):
        total += i


def func_b():
    total = sum(range(20_000_000))


result = compare_functions(func_a, func_b, runs=3)

print("\nComparison Result:\n")

for key, value in result.items():
    print(key, ":", value)
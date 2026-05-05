from profiler.comparison import compare_multiple


def func_a():
    total = 0
    for i in range(20_000_000):
        total += i


def func_b():
    total = sum(range(20_000_000))


def func_c():
    total = 0
    i = 0
    while i < 20_000_000:
        total += i
        i += 1


results = compare_multiple([func_a, func_b, func_c], runs=3)

print("\n=== Ranking ===\n")

for i, r in enumerate(results, start=1):
    print(f"{i}. {r['name']} → {r['energy']:.6f} J")
    
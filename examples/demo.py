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
import time
import psutil


def measure_function(func, tdp=28):
    process = psutil.Process()

    cpu_before = process.cpu_times().user + process.cpu_times().system
    wall_start = time.perf_counter()

    func()

    wall_end = time.perf_counter()
    cpu_after = process.cpu_times().user + process.cpu_times().system

    cpu_time = cpu_after - cpu_before
    wall_time = wall_end - wall_start
    energy = cpu_time * tdp

    return {
        "cpu_time": cpu_time,
        "wall_time": wall_time,
        "energy": energy
    }
def average_results(results):
    n = len(results)

    return {
        "cpu_time": sum(r["cpu_time"] for r in results) / n,
        "wall_time": sum(r["wall_time"] for r in results) / n,
        "energy": sum(r["energy"] for r in results) / n
    }
def compare_functions(func1, func2, runs=5, tdp=28):
    results1 = []
    results2 = []

    for _ in range(runs):
        results1.append(measure_function(func1, tdp))
        results2.append(measure_function(func2, tdp))

    avg1 = average_results(results1)
    avg2 = average_results(results2)

    # Decide winner
    if avg1["energy"] < avg2["energy"]:
        winner = func1.__name__
    else:
        winner = func2.__name__

    return {
        "function_1": {
            "name": func1.__name__,
            **avg1
        },
        "function_2": {
            "name": func2.__name__,
            **avg2
        },
        "winner": winner
    }
def compare_multiple(functions, runs=5, tdp=28):
    all_results = []

    for func in functions:
        run_results = []

        for _ in range(runs):
            run_results.append(measure_function(func, tdp))

        avg = average_results(run_results)

        all_results.append({
            "name": func.__name__,
            "cpu_time": avg["cpu_time"],
            "wall_time": avg["wall_time"],
            "energy": avg["energy"]
        })

    # Sort by energy (lowest = best)
    ranked = sorted(all_results, key=lambda x: x["energy"])

    return ranked
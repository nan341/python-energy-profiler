import time
import psutil


def profile_time(func):
    def wrapper(*args, **kwargs):
        process = psutil.Process()

        process.cpu_percent(interval=None)  # warm-up

        start_time = time.perf_counter()
        cpu_before = process.cpu_percent(interval=None)

        result = func(*args, **kwargs)

        cpu_after = process.cpu_percent(interval=None)
        end_time = time.perf_counter()

        execution_time = end_time - start_time
        avg_cpu = (cpu_before + cpu_after) / 2

        print(f"{func.__name__}:")
        print(f"  Time: {execution_time:.6f} sec")
        print(f"  CPU (approx): {avg_cpu:.2f}%")

        return result

    return wrapper
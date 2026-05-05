import time
import psutil


def profile_time(tdp=28):
    def decorator(func):
        def wrapper(*args, **kwargs):
            process = psutil.Process()

            # CPU time before
            cpu_before = process.cpu_times().user + process.cpu_times().system
            wall_start = time.perf_counter()

            result = func(*args, **kwargs)

            # CPU time after
            cpu_after = process.cpu_times().user + process.cpu_times().system
            wall_end = time.perf_counter()

            cpu_time = cpu_after - cpu_before
            wall_time = wall_end - wall_start

            # Utilization (for insight, not core model)
            cpu_util = (cpu_time / wall_time) if wall_time > 0 else 0

            # 🔥 Core energy model
            energy = cpu_time * tdp
            

            print(f"{func.__name__}:")
            print(f"  Wall Time: {wall_time:.6f} sec")
            print(f"  CPU Time: {cpu_time:.6f} sec")
            print(f"  CPU Utilization : {cpu_util * 100:.2f}%")
            print(f"  Estimated Energy: {energy:.6f} J (TDP={tdp}W)\n")
            

            return result

        return wrapper
    return decorator
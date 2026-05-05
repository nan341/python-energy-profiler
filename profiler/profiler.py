import time
import psutil
import threading


def profile_time(tdp=28):
    def decorator(func):
        def wrapper(*args, **kwargs):
            process = psutil.Process()

            cpu_samples = []
            running = True

            def sample_cpu():
                while running:
                    cpu = process.cpu_percent(interval=0.05)
                    cpu_samples.append(cpu)

            sampler_thread = threading.Thread(target=sample_cpu)

            start_time = time.perf_counter()
            sampler_thread.start()

            result = func(*args, **kwargs)

            running = False
            sampler_thread.join()
            end_time = time.perf_counter()

            execution_time = end_time - start_time
            avg_cpu = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0

            energy = (avg_cpu / 100) * execution_time * tdp

            print(f"{func.__name__}:")
            print(f"  Time: {execution_time:.6f} sec")
            print(f"  Avg CPU: {avg_cpu:.2f}%")
            print(f"  Estimated Energy: {energy:.6f} J (TDP={tdp:.2f}W)\n")

            return result

        return wrapper
    return decorator
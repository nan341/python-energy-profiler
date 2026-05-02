import time


def profile_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()

        execution_time = end_time - start_time

        print(f"{func.__name__} executed in {execution_time:.6f} seconds")

        return result

    return wrapper
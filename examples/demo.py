print("STARTED")

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from profiler.profiler import profile_time


@profile_time
def test_function():
    total = 0

    for i in range(10_000_000):
        total += i

    return total


test_function()

print("FINISHED")
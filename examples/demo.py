from profiler.calibration import calibrate_tdp
from profiler.profiler import profile_time


# Step 1: calibrate TDP
tdp_eff = calibrate_tdp()


# Step 2: use calibrated TDP
@profile_time(tdp=28)
def test_function():
    total = 0
    for i in range(20_000_000):
        total += i
    return total


print("STARTED\n")
test_function()
print("FINISHED")
import time
import psutil


def heavy_work():
    # Strong CPU workload
    for _ in range(200):
        sum(i * i for i in range(200_000))


def calibrate_tdp(nominal_tdp=28, duration=3):
    process = psutil.Process()

    # Warm-up
    process.cpu_percent(interval=None)

    cpu_samples = []
    start = time.perf_counter()

    print("\n[Calibration Started]\n")

    while time.perf_counter() - start < duration:
        heavy_work()  # keep CPU busy
        cpu = process.cpu_percent(interval=None)
        cpu_samples.append(cpu)

    avg_cpu = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0

    correction_factor = avg_cpu / 100
    calibrated_tdp = nominal_tdp * correction_factor

    print("[Calibration Results]")
    print(f"  Avg CPU: {avg_cpu:.2f}%")
    print(f"  Correction factor: {correction_factor:.3f}")
    print(f"  Calibrated TDP: {calibrated_tdp:.2f} W\n")

    return calibrated_tdp
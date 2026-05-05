# Development Log

## Stage 1 — Execution Time Profiling

Built a basic execution-time profiler using a Python decorator and `time.perf_counter()`.

Key things learned:
- decorators replace function references
- wrappers delay execution until runtime
- difference between decoration time and execution time

Issues faced:
- Python import/package structure issues
- fixed using `__init__.py`

## Stage 2 — Naive CPU Usage Estimation

Added process-level CPU usage tracking using `psutil.Process()`.

### Approach

Measured CPU usage using two snapshots:
- before function execution
- after function execution

Estimated average CPU usage as:
(avg_cpu = (cpu_before + cpu_after) / 2)

### Observations

- CPU readings vary significantly between runs for the same function
- Results are inconsistent and sensitive to timing
- Short executions produce especially unreliable values

### Limitation

This method does not capture CPU usage during execution.
It only samples at two points, which leads to poor approximation.

### Conclusion

Snapshot-based CPU estimation is unstable and insufficient
for reliable profiling.

### Next Step

Implement continuous CPU sampling during execution
(using a parallel/threaded approach) to improve accuracy.

## Stage 3 — Threaded CPU Sampling

Replaced snapshot-based CPU estimation with continuous sampling using a background thread.

### Approach

- Started a separate thread to record CPU usage at regular intervals (~50ms)
- Sampling runs in parallel while the target function executes
- Collected multiple CPU readings during execution
- Computed average CPU usage across all samples

### Observations

- CPU readings are significantly more stable compared to previous method
- CPU-bound functions now show values close to full utilization (~90–100%)
- Results are more consistent across repeated runs

### Limitation

- Sampling interval affects accuracy and overhead
- Very short functions may not produce enough samples
- Sampling thread introduces slight additional CPU usage

### Conclusion

Continuous sampling provides a much more reliable approximation of CPU usage
compared to snapshot-based measurement.

### Next Step

Use this improved CPU measurement to estimate energy consumption
using a TDP-based model.

## Stage 4 — Energy Estimation (TDP-based)

Extended the profiler to estimate energy consumption using execution time, CPU usage, and an assumed CPU TDP value.

### Approach

- Used average CPU usage obtained from continuous sampling
- Measured execution time using `time.perf_counter()`
- Applied simplified model:

  Energy ≈ CPU × Time × TDP

- Converted CPU percentage to fractional usage before calculation

### Observations

- Estimated energy increases proportionally with execution time
- CPU-bound workloads produce higher energy values as expected
- Smaller workloads result in significantly lower energy estimates
- Results are consistent across repeated runs

### Limitation

- TDP is a theoretical upper bound, not actual power consumption
- Model does not account for dynamic frequency scaling or system overhead
- Absolute energy values may be overestimated

### Conclusion

The model provides a consistent and useful approximation of energy consumption,
suitable for comparing relative computational cost between functions.

### Next Step

Refine the model by introducing calibration or normalization techniques
to improve realism of energy estimates.
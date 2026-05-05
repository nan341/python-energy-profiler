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

## Stage 5 — Empirical TDP Calibration

Introduced an empirical approach to refine the nominal TDP value based on observed system behavior under sustained load.

### Approach

- Started with nominal TDP (28W) based on CPU specifications
- Designed a CPU-intensive calibration workload to push utilization close to 100%
- Measured average CPU usage during the calibration run
- Derived a correction factor and computed an effective TDP value

### Observations

- CPU utilization during calibration reached ~98–99%, indicating a properly CPU-bound workload
- Calibrated TDP (~27.6W) is very close to nominal value (28W)
- Results are consistent across runs under similar system conditions

### Limitation

- Calibration does not measure actual hardware power consumption
- Results depend on workload design and system state (background processes, thermal conditions)
- Effective TDP represents behavior under high load, not all usage scenarios

### Conclusion

Empirical calibration validates that the system can reach near-nominal TDP under sustained CPU-bound workloads.
This improves confidence in the energy estimation model rather than significantly altering the base TDP value.

### Next Step

Build a comparison engine to evaluate multiple functions using averaged results
for more stable and meaningful energy and performance analysis.

## Stage 6 — Transition to CPU-Time-Based Energy Model

Refactored the energy estimation approach to use CPU time directly instead of sampled CPU utilization.

### Approach

- Measured CPU time using `psutil.Process().cpu_times()` (user + system time)
- Measured wall-clock time using `time.perf_counter()`
- Removed dependency on sampled CPU percentage and threaded sampling
- Updated energy model to:

  Energy ≈ CPU Time × TDP

### Observations

- CPU time closely tracks actual computational work performed
- For CPU-bound workloads, CPU time is nearly equal to wall time (~98–99%)
- Eliminates noise and variability introduced by periodic CPU sampling
- Simplifies implementation by removing threading and sampling logic

### Limitation

- Does not explicitly capture multi-core distribution of work
- Still relies on nominal TDP rather than real-time power measurement
- Less informative for I/O-bound or idle-heavy workloads

### Conclusion

Using CPU time provides a more direct and principled representation of computational effort.
This results in a simpler, more stable, and more interpretable energy estimation model compared to sampled CPU usage.

### Next Step

Develop a comparison engine to evaluate multiple functions using repeated runs and averaged results
for more reliable performance and energy analysis.

## Stage 7 — Function Comparison Engine

Implemented a comparison engine to evaluate multiple functions based on CPU time and estimated energy consumption.

### Approach

- Created a reusable measurement function using CPU-time-based profiling
- Ran each function multiple times to reduce noise
- Averaged CPU time, wall time, and energy across runs
- Compared functions based on average energy consumption
- Returned structured results including a winner

### Observations

- Optimized implementations (e.g., built-in functions) consistently outperform manual Python loops
- Energy consumption scales proportionally with CPU time
- Averaging across runs improves stability of results

### Limitation

- Sequential execution may introduce minor bias due to system state changes
- Results depend on workload type (CPU-bound vs I/O-bound)
- Does not yet support multi-function ranking beyond pairwise comparison

### Conclusion

The comparison engine transforms the profiler from a measurement tool into a decision-making system,
allowing direct evaluation of different implementations based on energy efficiency.

### Next Step

Improve output formatting and extend comparison to multiple functions with ranking support.
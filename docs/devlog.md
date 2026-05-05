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
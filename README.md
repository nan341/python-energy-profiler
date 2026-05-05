# Python Energy Profiler

An exploratory tool to compare Python functions based on estimated energy consumption using CPU time as a proxy for computational effort.

---

## Core Idea

Energy ≈ CPU Time × TDP

- CPU Time is measured using `psutil` (user + system time)
- TDP (Thermal Design Power) is used as a constant scaling factor
- The goal is to compare relative energy usage across different implementations

---

## What it Does

- Takes a Python file as input
- Extracts all user-defined functions
- Runs each function multiple times
- Measures CPU time and estimates energy
- Ranks functions based on energy consumption

---

## Example

```bash
python cli.py compare examples/sample.py --runs 5

output: 
1. fast_function -> 0.12 J
2. slow_function -> 0.45 J

Key Insight

Functions that perform more computation (higher CPU time) consistently show higher estimated energy usage.
This makes CPU time a useful and stable proxy for comparing implementations

Limitations
Estimates relative energy, not actual hardware consumption
Assumes a constant TDP (does not model dynamic CPU behavior)
Does not explicitly account for multi-core execution
Works best for CPU-bound workloads
Functions must not require input argument

PROJECT STRUCTURE
profiler/        # core measurement + comparison logic
cli/             # command-line interface
examples/        # sample functions
DEVLOG.md        # development process and experiments

Development Notes

This project evolved through multiple approaches (CPU sampling, tracing, etc.) before settling on a CPU-time-based model for stability and simplicity.
see devlog.md for full details.



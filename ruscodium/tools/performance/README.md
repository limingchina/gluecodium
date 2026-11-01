# C++ pipeline performance experiment

Run on Linux with Python 3, a C compiler, Java 17, an installed Gluecodium
`gluecodium/build/install/gluecodium/lib` distribution, and the Rust toolchain.
The native release must be rebuilt from the intended revision before measuring.
Start with an otherwise idle host and a new work directory on the intended
output filesystem. For the recorded environment:

```sh
source /workspace/.ruscodium-env/activate
source /workspace/.gluecodium-env/activate
(cd ruscodium && cargo build --offline --release)
cc -O2 -std=c11 -Wall -Wextra -Werror ruscodium/tools/performance/supervisor.c -o ruscodium/tools/performance/supervisor
python3 ruscodium/tools/performance/benchmark.py pilot --work /tmp/ruscodium-perf-new
python3 ruscodium/tools/performance/benchmark.py measure --work /tmp/ruscodium-perf-new
python3 ruscodium/tools/performance/warm.py --work /tmp/ruscodium-perf-new
```

`pilot.json`, `fresh.json`, and `warm.json` are the raw artifacts. The pilot
uses the actual JVM main and native `compile-cpp`, with caching off and complete
file bytes and path inventories checked for equality. It records a 60-second
per-invocation limit. If 500 structs times out it also pilots 125 structs.
Every parity-passing pilot is included, regardless of relative speed. Each JVM receives a new, writable `-Duser.home` directory prepared outside the timer so its default Java logging handler can initialize successfully; logging initialization failures invalidate that invocation. The
normalized default fixture corrects the missing required field-constructor
parameters; custom uses the original auxiliary file and custom options. Scale
inputs are generated independent one-field structs, not representative projects.
The 125-struct fixture is prepared in advance but only piloted on a 500 timeout.

Before timing, `measure` checks binary, jar, template, runner and input hashes
against the pilot; it stores the balanced, randomized eight-pair schedule
before any warmup or sample. Each invocation has its own initially nonexistent
output directory. Each generated tree is checked outside the timer against the
entire pilot inventory. Failures remain in the JSON and invalidate the sample.
Never reuse a work directory for a new run. The native C supervisor launches
one target process, waits with `wait4`, and reports `CLOCK_MONOTONIC` elapsed
wall, user/system CPU, and Linux `ru_maxrss` in KiB; timeout kills the target
process group. Its small fork origin avoids Python's resident-memory high-water
mark contaminating short-lived target peak RSS. Output is buffered filesystem
writes, not an fsync durability measurement. Statistics use interpolated
quartiles at `(n - 1) * p`; CPU total is the sum within each invocation.

The fresh-process result includes startup and starts a new JVM each time; file
caches have been warmed, but JIT state is not retained. The separate `warm.py`
experiment compiles tiny API drivers and repeats full load, validation,
generation and writes in each persistent process. It uses 10 recorded warmups
and 10 timed iterations, parses fixed options outside iteration timers and
verifies every output against the pilot. It includes 10 and 100 struct probes
only if both corresponding fresh pilot invocations finish in at most 3 seconds;
500 is excluded to bound run time. It records only per-iteration wall time:
process-lifetime RSS and CPU cannot be assigned to individual iterations.
Java `Gluecodium.execute()` runs broader validators than the native supported
subset. Even byte-identical output does not imply equal validation obligations,
full port parity, or isolate language/runtime overhead.

The reviewed report is [PERFORMANCE.md](../../PERFORMANCE.md). The active files
under `results/` are the corrected writable-Java-home run; the earlier logging
failure run remains under `results/initial-logging-error/` as historical evidence.
To regenerate the runtime/RSS chart, install Matplotlib and run
`python3 ruscodium/tools/performance/plot.py` from the repository root. Plotting
is outside measurement and validates that all displayed samples passed parity,
exit and logging gates.

# C++ generation optimization comparison

The optimized Rust generator completed all six workloads and matched the JVM output inventories. On 100 structs, the same-host median fell from 20.844 s to 0.089 s (234.7×); on 125 structs it fell from 44.499 s to 0.157 s (283.2×). The optimized 500-struct median was 1.296 s; the baseline hit its predeclared 60 s cap, so there is no baseline/optimized ratio for that workload. These are bounded observations on a shared host, not a general language benchmark.

## Fresh-process wall time

Each completed baseline has three samples; optimized Rust and JVM have eight each. Values are median [Q1, Q3] in seconds. Ratios divide the baseline or JVM median by the optimized median. Quartiles interpolate at `(n - 1) * p`; raw data also retain minima, maxima, CPU and RSS distributions.

| Workload | Baseline Rust, s | Optimized Rust, s | JVM, s | Baseline / optimized | JVM / optimized |
|---|---:|---:|---:|---:|---:|
| custom | 0.121 [0.117, 0.128] | 0.014 [0.012, 0.018] | 1.211 [1.161, 1.325] | 8.5× | 84.8× |
| default-normalized | 0.208 [0.180, 0.231] | 0.016 [0.014, 0.017] | 1.433 [1.285, 1.685] | 13.2× | 90.9× |
| structs-10 | 0.158 [0.141, 0.168] | 0.014 [0.013, 0.017] | 1.342 [1.153, 1.591] | 11.5× | 97.7× |
| structs-100 | 20.844 [18.661, 21.860] | 0.089 [0.078, 0.092] | 1.617 [1.307, 2.036] | 234.7× | 18.2× |
| structs-125 | 44.499 [42.981, 44.840] | 0.157 [0.133, 0.182] | 1.617 [1.500, 1.827] | 283.2× | 10.3× |
| structs-500 | censored at 60 s | 1.296 [1.196, 1.452] | 2.776 [2.532, 3.241] | — | 2.1× |

The baseline 500 attempt was killed at 60.009 s (signal 9; CPU 44.340 s; peak RSS 107,512 KiB). It produced no output tree. This single censored pilot is retained and is not a completed timing or parity result.

Median CPU seconds and peak RSS KiB for the completed trials are shown in baseline / optimized / JVM order:

| Workload | CPU seconds | Peak RSS KiB |
|---|---:|---:|
| custom | 0.091 / 0.012 / 1.341 | 5,976 / 5,558 / 98,676 |
| default-normalized | 0.144 / 0.015 / 1.455 | 6,924 / 6,340 / 104,728 |
| structs-10 | 0.125 / 0.014 / 1.294 | 5,668 / 5,158 / 91,706 |
| structs-100 | 16.379 / 0.085 / 1.647 | 24,588 / 20,584 / 110,120 |
| structs-125 | 35.309 / 0.112 / 1.685 | 29,748 / 24,616 / 108,762 |
| structs-500 | — / 0.991 / 2.978 | — / 88,070 / 167,464 |

## Output and measurement gate

The six JVM reference preflights and all 111 completed scheduled invocations succeeded and matched their reference inventories. Every inventory covers the entire output tree, including common files: relative paths, byte lengths and per-file SHA-256 hashes are retained for every preflight and completed output in the [raw comparison](tools/performance/optimization-results/optimization.json). The reference trees contain 24, 26, 38, 218, 268 and 1,018 files respectively in the order above. Source and output counts, commands, the predeclared randomized schedule, failures, host metadata and before/after executable, input, jar, template, runner and supervisor identities are recorded there; identities matched at the end.

The schedule was written before any invocation: six reference preflights, eight balanced JVM/optimized pairs per workload, three baseline attempts per first five workloads, and one capped baseline 500 attempt. All targets were spawned by the same small native C supervisor; `CLOCK_MONOTONIC` and `wait4` supplied wall, per-child CPU and peak RSS. JVM processes used freshly created writable homes. Each output directory was new; hashing and comparison ran outside timers. The output filesystem was tmpfs, and writes were buffered without an fsync durability guarantee. Fresh processes include JVM startup, with warm filesystem caches but no persistent JIT state. The separate preflights are excluded from sample statistics.

The fixtures and production templates match [M13](PERFORMANCE.md). Default-normalized corrects the field-constructor arguments in a copied input so the JVM validator accepts it. Synthetic independent structs are scaling probes rather than representative projects. The JVM performs broader validation than the native supported subset, so matching output for these fixtures does not establish complete compiler parity. The small samples and shared host limit interpretation; these timings do not isolate language or runtime overhead.

## Baseline operation counts

A separate instrumented baseline, built from the same source revision, counted 39 graph imports, 58 C++ resolver constructions, 204 file/partial parses and 8,089,290 graph-import absence-node probes for 10 structs. For 100 structs the counts were 219, 418, 1,734 and 2,183,649,930 respectively. Both instrumented outputs matched the M13 JVM inventories. The absence probe count applies only to graph-import absence validation, not other checks: on a successful import an early match would have returned an error, so the instrumentation adds `node count × absent-name count` per import. These are operation counts, not sampled time attribution; the instrumented binary was never used for timing. The prepared renderer reuses graph, resolver and parsed-template state and indexes class properties during absence validation. See [counts and commands](tools/performance/optimization-results/counts.json), the [exact historical instrumentation](tools/performance/optimization-results/instrument-baseline-original.py), and the [parameterized reproduction script](tools/performance/instrument-baseline.py).

## Reproduction and environment

Recorded UTC: 2026-11-02 04:14:50–04:20:59. Linux 6.18.57, Xeon Platinum 8573C, affinity CPUs 0–2, cgroup quota two CPUs and 8 GiB memory limit, tmpfs outputs; Temurin 17.0.16+8 and rustc 1.99.1. The clean baseline was archived from commit `15b1db4c48ef0fbf7a86aefa6750f6ebcd5a5e88` and built with `cargo build --offline --release`; SHA-256 `10585d3f82151cec742b7f5dacbe2b91902901e66df69b583f673f6a6ed8d697`, identical to the M13 binary. The optimized build at `ec381af93117e66f583c1ea21cb339d9586a1bca` has SHA-256 `10a2e27ce4750bc1e7d961b04bdae204c943722494998d8aa07c8aafcc00f716`.

From the repository root, with the installed Gluecodium distribution and Rust toolchain available, use new empty directories and an otherwise idle Linux host:

```sh
source /workspace/.ruscodium-env/activate
source /workspace/.gluecodium-env/activate
mkdir -p /tmp/ruscodium-baseline-build
git archive 15b1db4c48ef0fbf7a86aefa6750f6ebcd5a5e88 ruscodium | tar -x -C /tmp/ruscodium-baseline-build
cargo build --offline --release --manifest-path /tmp/ruscodium-baseline-build/ruscodium/Cargo.toml
cargo build --offline --release --manifest-path ruscodium/Cargo.toml
cc -O2 -std=c11 -Wall -Wextra -Werror ruscodium/tools/performance/supervisor.c -o ruscodium/tools/performance/supervisor
python3 ruscodium/tools/performance/optimization.py --work /tmp/ruscodium-optimization-new \
  --baseline /tmp/ruscodium-baseline-build/ruscodium/target/release/ruscodium \
  --optimized ruscodium/target/release/ruscodium
```

For the diagnostic source, use `python3 ruscodium/tools/performance/instrument-baseline.py --repo "$PWD" --work /tmp/ruscodium-count-source`; build that isolated tree and run the two synthetic fixtures as described by the recorded count commands. The instrumentation changes only the isolated source and the reproduction script verifies its expected insertion sites. Never substitute its instrumented binary for either timed executable.

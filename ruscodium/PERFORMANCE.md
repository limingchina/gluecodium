# C++ pipeline performance comparison

On these five parity-checked inputs, fresh Rust processes were faster for the two real fixtures and 10 simple structs. At 100 and 125 structs the JVM was faster. Rust used less peak resident memory on every completed workload. This is a bounded experiment on a shared host and does not establish complete compiler parity or a general language benchmark.

## Fresh process, warm filesystem

Each row summarizes eight independent processes per implementation, paired in a fixed-seed balanced randomized order. Each metric is **median [Q1, Q3]; min–max**. Wall and CPU are seconds; peak RSS is KiB. CPU is per-invocation user + system time. Quartiles interpolate at `(n - 1) * p`. The ratio is JVM median wall divided by Rust median wall; values above 1 favor Rust.

| Workload | Implementation | Wall seconds | CPU seconds | Peak RSS KiB | JVM / Rust wall |
|---|---|---:|---:|---:|---:|
| custom | jvm | 1.157 [1.096, 1.262]; 0.966–1.471 | 1.309 [1.175, 1.348]; 1.132–1.464 | 94366 [93046, 96134]; 89772–100680 | 15.178 |
| custom | rust | 0.076 [0.064, 0.103]; 0.061–0.116 | 0.064 [0.061, 0.066]; 0.060–0.091 | 5980 [5964, 5980]; 5900–6040 | 15.178 |
| default-normalized | jvm | 1.533 [1.201, 1.711]; 1.183–2.095 | 1.429 [1.358, 1.566]; 1.256–1.744 | 104438 [104154, 105604]; 101688–108904 | 9.586 |
| default-normalized | rust | 0.160 [0.139, 0.258]; 0.102–0.315 | 0.123 [0.100, 0.145]; 0.097–0.148 | 6972 [6951, 7055]; 6940–7064 | 9.586 |
| structs-10 | jvm | 1.172 [1.116, 1.248]; 0.898–1.856 | 1.214 [1.170, 1.246]; 1.043–1.415 | 87994 [84748, 92795]; 83264–95364 | 8.586 |
| structs-10 | rust | 0.136 [0.126, 0.189]; 0.116–0.239 | 0.120 [0.089, 0.125]; 0.084–0.126 | 5688 [5675, 5724]; 5644–5724 | 8.586 |
| structs-100 | jvm | 1.488 [1.371, 1.576]; 1.196–1.761 | 1.531 [1.450, 1.560]; 1.341–1.780 | 106800 [102397, 110332]; 101504–116528 | 0.077 |
| structs-100 | rust | 19.215 [18.524, 20.528]; 16.250–23.539 | 13.235 [12.906, 16.487]; 12.822–17.294 | 24632 [24615, 24668]; 24472–24728 | 0.077 |
| structs-125 | jvm | 1.643 [1.589, 1.914]; 1.460–2.124 | 1.722 [1.676, 1.779]; 1.459–2.254 | 115732 [111675, 117264]; 107568–118768 | 0.039 |
| structs-125 | rust | 42.094 [40.125, 43.499]; 31.363–48.014 | 31.673 [30.696, 34.873]; 24.389–35.496 | 29850 [29768, 29916]; 29620–29976 | 0.039 |

The 500-struct pilot completed on the JVM in 3.224 s but the Rust process hit the predeclared 60 s limit (60.034 s, killed with signal 9). Its output was not available for comparison; no parity or speed ratio is claimed. The 125-struct intermediate was specified before the pilot and included after that timeout. Exact pilot commands, censored result, file inventories and every timed sample are in the raw artifacts.

## Inputs and output gate

| Workload | Source bytes / lines | Top-level declarations | Output files / bytes |
|---|---:|---:|---:|
| custom | 354 / 15 | 3 | 24 / 75,502 |
| default-normalized | 525 / 21 | 5 | 26 / 73,675 |
| structs-10 | 335 / 12 | 10 | 38 / 78,333 |
| structs-100 | 3,125 / 102 | 100 | 218 / 157,263 |
| structs-125 | 3,900 / 127 | 125 | 268 / 179,188 |
| structs-500 (JVM only; Rust timed out) | 15,525 / 502 | 500 | 1018 / 508,063 |

The custom workload uses the repository fixture, auxiliary input, custom namespaces, exports and copyright. The default fixture is a copy in which `field constructor(label)` is changed to `field constructor(label, mapping, tags)` so the full JVM validator accepts it; the original is unchanged. Synthetic scale workloads contain independent one-field structs and are controlled probes, not representative projects. Identical complete paths and bytes, including common files, were required before sampling. All 80 timed outputs were checked against that baseline after each timer stopped and matched. Inventories and per-file SHA-256 hashes are retained in [pilot.json](tools/performance/results/pilot.json).

## Persistent process experiment

The separate API test repeats full load, validation, generation and writing within one process per implementation using the 10-struct workload. Fixed options are parsed before the iteration timer; every iteration writes to a new directory. After 10 recorded warmup iterations, the next 10 produced the following wall times in seconds (median [Q1, Q3]; min–max):

- jvm: 0.0327 [0.0235, 0.0497]; 0.0151–0.0637
- rust: 0.1367 [0.1230, 0.1610]; 0.1147–0.1983

The JVM/Rust median ratio is 0.239: in this small persistent-process experiment the JVM was about 4.2 times faster. These iterations are correlated within one process per implementation; 10 warmups do not prove JIT steady state. They are not a subtraction of startup cost from the fresh CLI results. Per-iteration CPU and memory were not measured. The 100-struct case exceeded the preset 3-second pilot budget for repeated API measurements; 500 was excluded by the budget rule. All 40 iteration outputs matched the fresh baseline. The initial Java setup failed because its output parent did not exist; the failure is retained in [warm-setup-failure.json](tools/performance/results/warm-setup-failure.json), and the parent was created outside the timer for the successful rerun.

## Method and limits

The JVM command invokes installed Gluecodium 14.2.2 through `com.here.gluecodium.Gluecodium` with `-generators cpp` and caching disabled. The native command is the rebuilt optimized `ruscodium compile-cpp`; both read LIME and write fresh full C++ output trees. Neither consumes an oracle export or pre-parsed model. Builds, fixture preparation and output hashing are outside the timers. JVM validation is broader than the native adapter’s guarded supported subset; matching generated bytes for these inputs does not equal matching every semantic obligation. Native rendering repeatedly imports the graph for generated files, which may contribute to its observed scaling; this experiment does not isolate a cause or language overhead.

Each fresh trial starts a new process and a new JVM: warmed filesystem caches do not mean warmed JVM JIT state. Linux `CLOCK_MONOTONIC` and per-child `wait4` provide wall, user/system CPU and peak RSS, with an independently launched small native supervisor. Output writes are buffered and do not include an fsync durability guarantee. Ranges reflect a small sample on a shared host, not statistical significance.

Pilot UTC: 2026-11-01T21:19:46.002402+00:00. Linux 6.18.57, Xeon Platinum 8573C, three CPUs in process affinity, cgroup quota two CPUs and 8 GiB memory limit, tmpfs output. Temurin 17.0.16+8 and rustc 1.99.1 were used. The native binary was built with `cargo build --offline --release` from the compiler source at `141fe1cd5` (identical to `12e45a188`; the intervening commit only updates planning), before the benchmark-only harness commit `9f599c55a`. Native SHA-256: `10585d3f82151cec742b7f5dacbe2b91902901e66df69b583f673f6a6ed8d697`; JVM application jar SHA-256: `fe1bda6ef33ef0abdf6c99abb3af9897b0307bb21050e107563368e7b2a8fac2`. Environment metadata and individual jar, template, binary, input and options hashes are recorded in the JSON. The original 315 production templates were retained.

Reproduction steps and the exact boundaries are in [the benchmark README](tools/performance/README.md). Raw [pilot](tools/performance/results/pilot.json), [fresh-process](tools/performance/results/fresh.json) and [persistent-process](tools/performance/results/warm.json) JSON include commands, schedule, diagnostics, samples and host metadata.

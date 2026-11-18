# Data dictionary

`n` and `t` are the number of regulators and recovery threshold, respectively
(the manuscript uses n_E and t_E). Trials are indexed by `trial`. Payload size
is `message_bytes`; 1 KB = 1024 bytes and 1 MB = 1,048,576 bytes.

## Complete-path JSON

`samples` contains STRD observations and `baseline_samples` contains baseline
observations. All timing fields in these arrays are milliseconds:

- `signcrypt`: complete measured local signcryption path.
- `receiver`: recipient decryption, including the proof-verification gate for STRD.
- `regulator`: threshold regulatory recovery and decryption.
- `contributions`: contribution generation and DLEQ verification.
- `certificate_issue`: local certificate issuance.
- `prove`: proof-generation call time with prover artifacts loaded.
- `issuance_verify`: verification before certificate issuance.

Fields ending in `_bytes`, and values under `artifact_bytes`, are byte counts.
`load_seconds` is a single initial worker-loading measurement in seconds.
`constraints` is the circuit constraint count. `complete` records completion
of the benchmark run. Metadata hashes identify sources and the benchmark binary.

## Collection JSON

`results` contains scenario summaries and `samples` per scenario. Configurations
are (3,2), (5,3), (9,3), (13,3), (13,5), and (13,7).
Scenario names are retained exactly as recorded. The three conditions are no
injected delay, heterogeneous delays cycling through 5/20/60 ms, and 20 ms
delay with a 20% response-drop probability. The seed 20261113 controls the
experiment's randomized scenario behavior; it is not a cryptographic secret.

`success` records completion; `elapsed_ms` records elapsed time, including
failed trials; `logical_bytes` counts application-layer logical bytes.
`mean_ms`, `median_ms` and `p95_ms` summarize successful trials.
`failure_mean_ms` summarizes failures and is null when no failure occurred.
The asynchronous `timeout_ms` wait budget excludes work outside the wait, so
it is not a bound on total wall-clock time. Completion batches can include
more than t responses; logical byte counts exclude transport/encryption overhead.

## CSVs and summary

In scheme CSVs, `auth` maps to `certificate_issue`, `tvrf` maps to
`contributions`; other timing columns retain their JSON meanings. Values are
five-trial means in milliseconds. In comparison CSVs, `metric` identifies the
path and `baseline`/`ours` contain mean milliseconds. `id` is a plotting index.
In the collection CSV, `mean` and `p95` are successful-trial milliseconds,
`successes` is a count out of 50, and `bytes` is the recorded mean logical byte
count. The summary JSON's `std_ms` uses sample standard deviation (n-1).

## Validation records

`current_run_validation.json` records aggregate trial counts and checked
functional properties. `benchmark_full_profile_3_2.json` records a separate
integration/negative-test run; its timing fields end in `_seconds`.
`full_profile_artifact_metrics.json` records one (3,2) setup/proving run and
artifact sizes, not repeated performance statistics. `fixed_circuit_simulation_results.json`
records simulator checks with fresh in-memory test setups. No keys, witnesses,
setup trapdoors, or binary artifacts are distributed in this repository.

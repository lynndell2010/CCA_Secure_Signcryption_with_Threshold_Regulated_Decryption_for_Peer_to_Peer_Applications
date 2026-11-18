# STRD experimental data

This repository provides the experimental measurements supporting **CCA Secure
Signcryption with Threshold-Regulated Decryption for Peer-to-Peer Applications**.
It contains data and numerical processing utilities. The unpublished manuscript,
proof text, submission documents, and internal review notes are not included.
The full protocol implementation is not included in this data release.

## Access

Browse or download the JSON and CSV files directly on GitHub, or select
**Code > Download ZIP**. No external dataset, account, or access request is
needed to read the public data. Cite the repository URL together with a commit
identifier to identify the exact version used.

## Contents and figure mapping

| File | Contents |
| --- | --- |
| `data/benchmark_current_3_2.json` | Raw STRD and baseline timings for n=3, t=2 |
| `data/benchmark_current_5_3.json` | Raw STRD and baseline timings for n=5, t=3 |
| `data/benchmark_current_p2p.json` | 900 single-host contribution-collection trials, including failed trials |
| `data/benchmark_current_summary.json` | Means, sample standard deviations, minima and maxima |
| `figures/scheme_1kb.csv` | Figure 2: local paths, 1 KB payload |
| `figures/scheme_1mb.csv` | Figure 3: local paths, 1 MB payload |
| `figures/threshold_compare_1kb.csv`, `figures/threshold_compare_1mb.csv` | Figure 4: STRD and threshold baseline |
| `figures/p2p_emulation.csv` | Figure 5: representative contribution-collection scenarios |
| `figures/current_manifest.json` | SHA-256 hashes of the processing script, raw inputs and generated CSVs |
| `validation/` | Recorded functional checks, fixed-circuit simulation checks, and artifact measurements |
| `SHA256SUMS` | Checksums of the files in this release |

The raw records include 20 STRD samples and 20 baseline samples: five trials
for each of two committee configurations and two payload sizes (1024 and
1,048,576 bytes). Collection records cover six configurations, three scenarios,
and 50 trials per combination. All measurements are retained as recorded.
Historical source/binary hashes identify the measurement snapshot; those
implementation files are not bundled here.

## Measurement scope

Measurements were recorded on an Apple M1 Pro with 16 GiB RAM, macOS 27.2.1,
and Python 3.9.6. Environment metadata and timestamps are stored in the JSON.
Local STRD timings include actual full-relation NIZK proving and verification.
The prover retains loaded circuit/proving artifacts; initial loading is recorded
separately. Setup and key registration precede timing. Certificate issuance uses
locally held test keys. Recipient and regulator timings include standalone
verifier startup and verifying-key loading. Subcomponent timings overlap the
signcryption total and must not be summed with it.

The baseline supplies independent recipient decryption, authentication and
threshold recovery, without the additional online authorization and aggregate
NIZK functions. Comparisons therefore measure the costs of added functionality.
Collection trials run separate processes on one host, with application-layer
delays and drops. Their timing scope is share collection, verification and
aggregation. Five local samples per case and 50 collection samples per case
characterize the observed runs, rather than general scaling or availability.
The `validation` records are functional evidence; single-run timings there are
not used for Figures 2–5 and do not establish cryptographic security.

## Regenerate numerical outputs

Only the Python standard library is required (Python 3.9 or later):

```sh
python3 generate_plot_data.py
```

This recomputes the complete-path summary and the five figure-input CSVs from
the supplied records. The collection CSV selects recorded scenario summaries;
the raw per-trial observations remain available in its source JSON. This does
not rerun cryptographic benchmarks or generate the manuscript's LaTeX plots.

See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for fields, units and scenarios.
